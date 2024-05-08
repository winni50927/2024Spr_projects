'''
Simulation of a series of 4 player game of Rummikub, a famous board game.
Uses basic Monte Carlo simulation techniques to derive
statistical analysis of this game scenario.

Author: Jui-Fang(Winni) Hsu

Usage: I recommend set up number of games up to 10000 games. Over 10000, the simulation will be time-costing.

Cite:
1. The idea of utilizing 1-52 to represent 1-13 in four suits comes from: Pei-Yi Ding http://squall.cs.ntou.edu.tw/cprog/practices/p05-3%20Poker%20hand%20ranking.pdf
2. The Object-Oriented-Design, stats, and Monte Carlo Simulation function of the Game are learned from: Professor Weible, MC_rock_paper_scissors.py
3. The method to handle the print control is learned from ChatCPT.
'''

# TODO: Speed up the game
# TODO: Randomize the play orders
# TODO: Adding adapitive strategies to players


import itertools
import operator


class Tile:
    def __init__(self, number):
        """
        Determine the value and suit of each tile.
        :param number: Numbers are 1-52 representing 1-13 for 4 suits
        >>> tile = Tile(52)
        >>> tile.number
        13
        """
        self.number = number % 13 if number % 13 != 0 else 13
        self.suit = self.determine_suit(number)

    def determine_suit(self, number):
        """
        :param number: Numbers are 1-13 for all suits
        :return: the category of suit
        """
        if 1 <= number <= 13:
            return 'Clover'
        elif 14 <= number <= 26:
            return 'Heart'
        elif 27 <= number <= 39:
            return 'Diamond'
        elif 40 <= number <= 52:
            return 'Spade'
        else:
            raise ValueError("Number out of valid range")

    def __repr__(self):
        return f"{self.suit[0]}{self.number}"


class Deck:
    def __init__(self):
        self.tiles = [Tile(number) for number in range(1, 53)] * 2  # Two sets of 1-52
        self.shuffle()

    def shuffle(self):
        import random
        random.shuffle(self.tiles)

    def draw(self, count=1):
        drawn_tiles = self.tiles[:count]
        self.tiles = self.tiles[count:]
        return drawn_tiles

class Player:
    def __init__(self, name, game=None):
        self.name = name
        self.game = game
        self.hand = []
        self.total_points = 0
        self.has_met_cold_start = False
        self.is_first_cold_start = False
        self.wins = 0
        self.losses = 0
        self.ties = 0

    def reset_stats(self):
        self.wins = 0
        self.losses = 0
        self.ties = 0
    def print(self, message):
        """Utility method to control print statements based on the game's verbosity."""
        if self.game and self.game.verbose:
            print(message)
    def draw_tiles(self, deck, count=1):
        drawn_tiles = deck.draw(count)
        self.print(f"{self.name} drew {len(drawn_tiles)} tiles.")
        self.hand.extend(drawn_tiles)

    def find_sets(self, hand):
        """Find all sets in the player's hand that are valid according to the game rules."""
        result = []
        # Sort hand by number, then by suit to keep the same numbers grouped and ordered.
        sorted_hand = sorted(hand, key=lambda x: (x.number, x.suit))
        for key, group in itertools.groupby(sorted_hand, key=lambda x: x.number):
            group_list = list(group)
            if len(group_list) >= 3:
                # Check if all cards in the group have unique suits
                suits = {card.suit for card in group_list}
                if len(suits) == len(group_list):
                    result.append(group_list)
        return result

    def find_runs(self, hand):
        """ Find all runs in the player's hand that are valid according to the game rules.
        >>> player = Player("Test Player")
        >>> tiles = [Tile(26), Tile(25), Tile(26), Tile(24), Tile(25)]
        >>> Player.find_runs(tiles)
        [24, 25, 26]
        """
        result = []
        for suit in ['Clover', 'Heart', 'Spade', 'Diamond']:
            sorted_hand = sorted([tile for tile in hand if tile.suit == suit], key=lambda x: x.number)

            # Process sorted hand to find runs
            if sorted_hand:
                current_run = [sorted_hand[0]]
                for i in range(1, len(sorted_hand)):
                    if sorted_hand[i].number == current_run[-1].number + 1:
                        current_run.append(sorted_hand[i])
                    elif sorted_hand[i].number == current_run[-1].number:
                        continue  # Skip duplicate numbers
                    else:
                        # Only add runs that are 3 or more tiles long
                        if len(current_run) >= 3:
                            result.append(current_run)
                        current_run = [sorted_hand[i]]

                # Check if the last collected run is valid
                if len(current_run) >= 3:
                    result.append(current_run)
        return result

    def find_melds(self, hand=None):
        """ Combine find_sets and find_runs to find all possible melds. """
        if hand is None:
            hand = self.hand
        sets = self.find_sets(hand)
        runs = self.find_runs(hand)
        all_melds = sets + runs
        return all_melds

    def play_best_meld(self):
        """Find and play the best meld based on tile values, returns True if a meld was played, False otherwise."""
        melds = self.find_melds()
        if melds:
            best_meld = max(melds, key=lambda m: sum(tile.number for tile in m))
            self.play_tiles(best_meld)
            return True
        return False

    def play_tiles(self, meld, game):
        """Remove meld from hand, and add it to the river."""
        for tile in meld:
            self.hand.remove(tile)
        self.print(f"{self.name} played: {meld}")  # Print each meld played
        game.update_river(meld)  # 更新 river 並打印當前狀態

    def find_runs_match_in_hand_and_river(self, game_river):
        """Find tiles in hand that can extend runs in the river."""
        extendable_runs = []
        for run in game_river:
            if isinstance(run, list) and self.is_run(run):
                first_tile = run[0]
                last_tile = run[-1]
                prev_number = first_tile.number - 1
                next_number = last_tile.number + 1

                for tile in self.hand:
                    if tile.suit == first_tile.suit and tile.number == prev_number:
                        extendable_runs.append((tile, run, 'head'))
                        while prev_number > 1:
                            prev_number -= 1
                            next_tile = next((t for t in self.hand if t.suit == tile.suit and t.number == prev_number),
                                             None)
                            if next_tile:
                                extendable_runs.append((next_tile, run, 'head'))
                            else:
                                break

                    if tile.suit == last_tile.suit and tile.number == next_number:
                        extendable_runs.append((tile, run, 'tail'))
                        while next_number < 13:
                            next_number += 1
                            next_tile = next((t for t in self.hand if t.suit == tile.suit and t.number == next_number),
                                             None)
                            if next_tile:
                                extendable_runs.append((next_tile, run, 'tail'))
                            else:
                                break

        return extendable_runs

    def is_run(self, tiles):
        if len(tiles) < 3:
            return False
        sorted_tiles = sorted(tiles, key=lambda x: x.number)
        return all(sorted_tiles[i].number + 1 == sorted_tiles[i + 1].number for i in range(len(sorted_tiles) - 1))

    def extend_run_play_tiles(self, extendable_runs, game_river):
        """Play the tiles that can extend runs in the river."""
        for tile, run, position in extendable_runs:
            if tile not in self.hand:
                self.print(f"Attempted to play {tile} which is not in hand. Skipping.")
                continue
            if position == 'head':
                run.insert(0, tile)  # 插入到Run的头部
            elif position == 'tail':
                run.append(tile)  # 添加到Run的尾部
            # print(f"Before removing, {self.name}'s hand: {[str(tile) for tile in self.hand]}")
            self.hand.remove(tile)  # 从手牌中移除该牌
            # print(f"After removing, {self.name}'s hand: {[str(tile) for tile in self.hand]}")
            self.print(f"{self.name} extended a run at the {position} with {tile}. Updated run: {run}")
            # game.update_river(tile)  # 更新 river 並打印當前狀態

    def insert_and_split_runs(self, game_river, game):
        """Find tiles in hand that can insert into runs in the river, and play them by inserting them in the rivers and
        separating the related melds."""
        changes_made = False
        new_river = game_river[:]  # 创建river的副本进行操作，避免直接修改原始列表
        for run in new_river:
            if len(run) >= 5 and self.is_run(run):
                for i in range(2, len(run) - 2):  # 避开头尾两张
                    middle_tile = run[i]
                    if middle_tile in self.hand:
                        # 切割并创建新的部分
                        left_part = run[:i + 1]
                        right_part = run[i:]
                        game.river.remove(run)
                        self.hand.remove(middle_tile)
                        game.river.append(left_part)
                        game.river.append(right_part)
                        changes_made = True
                        self.print(
                            f"{self.name} inserted {middle_tile} and split the run into {left_part} and {right_part}.")
                        break  # 处理完一个后即退出，防止重复操作
                if changes_made:
                    break  # 已经修改了river，无需进一步循环

        return changes_made

    ## find sets with in hands and river!!!

    def find_sets_match_in_hand_and_river(self, game_river):
        """Find the tiles that can join sets in the river."""
        extendable_sets = []
        for set_group in game_river:
            if isinstance(set_group, list) and self.is_set(set_group):
                needed_suits = {'Clover', 'Heart', 'Spade', 'Diamond'} - {tile.suit for tile in set_group}
                number = set_group[0].number
                # Check for tiles in hand that can be added to the set
                for tile in self.hand:
                    if tile.number == number and tile.suit in needed_suits:
                        extendable_sets.append((tile, set_group))
        return extendable_sets

    def is_set(self, tiles):
        if len(tiles) < 3:
            return False
        numbers = {tile.number for tile in tiles}
        return len(numbers) == 1 and len(tiles) <= 4

    def extendable_set_play_tiles(self, game, extendable_sets):
        """Play the tiles that can join sets in the river."""
        played_any = False
        for tile, set_group in extendable_sets:
            if tile not in self.hand:
                self.print(f"Attempted to play {tile} which is not in hand. Skipping.")
                continue
            set_group.append(tile)
            self.hand.remove(tile)
            game.update_river(set_group)  # Assuming game has a method to update river
            self.print(f"{self.name} added {tile} to a set in the river. Updated set: {set_group}")
            played_any = True
        return played_any

    # Find pairs
    def find_and_modify_runs_or_sets(self, game):
        played = False
        pairs = self.find_pairs_in_hand()
        for number, suits_needed in pairs:
            if self.modify_runs_and_create_set(game, number, suits_needed):
                played = True
        return played

    def find_pairs_in_hand(self):
        """Find pairs in hand"""
        counts = {}
        for tile in self.hand:
            if tile.number not in counts:
                counts[tile.number] = set()
            counts[tile.number].add(tile.suit)

        pairs = []
        for number, suits in counts.items():
            if len(suits) == 2:
                needed_suits = {'Clover', 'Heart', 'Spade', 'Diamond'} - suits
                pairs.append((number, needed_suits))
        return pairs

    def modify_runs_and_create_set(self, game, number, suits_needed):
        """修改river中的runs或sets，并尝试创建新的set"""
        for run in game.river[:]:
            if len(run) >= 4:
                for tile in [run[0], run[-1]]:  # 只检查头尾
                    if tile.number == number and tile.suit in suits_needed:
                        if self.create_and_add_new_set(game, run, number, tile.suit):
                            return True
            elif len(run) > 7:
                for tile in run[3:-3]:
                    if tile.number == number and tile.suit in suits_needed:
                        if self.split_run_and_add_new_set(game, run, tile):
                            return True
            elif len(run) == 4 and self.is_set(run):
                for tile in run:
                    if tile.number == number and tile.suit in suits_needed:
                        if self.remove_from_set_and_add_new_set(game, run, number, tile.suit):
                            return True
        return False

    def create_and_add_new_set(self, game, run, number, suit_to_remove):
        """从run中移除相应的牌，并与手牌中的两张牌创建新的set"""
        new_run = [tile for tile in run if not (tile.number == number and tile.suit == suit_to_remove)]
        new_set = [tile for tile in self.hand if tile.number == number]
        new_set.append(next(tile for tile in run if tile.number == number and tile.suit == suit_to_remove))

        if len(new_set) == 3:  # 确保有三张牌才能形成set
            for tile in new_set:
                if tile not in self.hand:
                    self.print(f"Attempted to play {tile} which is not in hand. Skipping.")
                    continue
                self.hand.remove(tile)  # 从手牌中移除使用的牌
            game.update_river(new_run)
            game.river.append(new_set)
            self.print(f"{self.name} created new set {new_set} and updated run {new_run}")
            return True
        return False

    def split_run_and_add_new_set(self, game, run, tile_to_remove):
        """将run从tile_to_remove处分开，并创建新的set"""
        index = run.index(tile_to_remove)
        left_part = run[:index]
        right_part = run[index + 1:]
        new_set = [tile for tile in self.hand if tile.number == tile_to_remove.number] + [tile_to_remove]
        for tile in new_set:
            if tile not in self.hand:
                self.print(f"Attempted to play {tile} which is not in hand. Skipping.")
                continue
            self.hand.remove(tile)
        game.update_river(left_part + right_part)
        game.river.append(new_set)
        self.print(f"{self.name} split run and created new set {new_set} at {tile_to_remove}")

    def remove_from_set_and_add_new_set(self, game, set_group, number, suits_needed):
        """从set中移除一张牌，并与手牌中的牌创建新的set"""
        new_set = [tile for tile in self.hand if tile.number == number] + [tile for tile in set_group if
                                                                           tile.suit in suits_needed]
        for tile in new_set:
            self.hand.remove(tile)
        new_group = [tile for tile in set_group if tile not in new_set]
        game.update_river(new_group)
        game.river.append(new_set)
        self.print(f"{self.name} modified set and created new set {new_set} from {set_group}")

    # Find Single-Set
    def find_single_set(self, game):
        played = False
        # Iterate over a copy of the hand to avoid modification issues while iterating
        for tile in self.hand[:]:
            potential_set = [tile]
            suits_needed = {'Clover', 'Heart', 'Spade', 'Diamond'} - {tile.suit}
            if self.find_matching_tiles(game.river, potential_set, suits_needed):
                if len(potential_set) == 3:
                    # Before removing, ensure the tile is still in the hand
                    if tile in self.hand:
                        self.hand.remove(tile)
                    for t in potential_set[1:]:
                        self.remove_tile_from_river(game, t)
                    game.river.append(potential_set)
                    self.print(f"{self.name} played a new set with tiles: {potential_set}")
                    played = True
        return played

    def find_matching_tiles(self, river, potential_set, suits_needed):
        # 检查river中的每一个run或set
        for group in river:
            if len(group) > 4:  # 检查长于4的runs
                # 检查run的头尾
                if group[0].number == potential_set[0].number and group[0].suit in suits_needed:
                    potential_set.append(group[0])
                    suits_needed.remove(group[0].suit)
                if group[-1].number == potential_set[0].number and group[-1].suit in suits_needed:
                    potential_set.append(group[-1])
                    suits_needed.remove(group[-1].suit)
            if len(potential_set) == 3:
                return True  # 已经组成一个set
            # 检查长于7的runs中间的牌
            if len(group) > 7:
                for tile in group[3:-3]:
                    if tile.number == potential_set[0].number and tile.suit in suits_needed:
                        # 如果找到匹配的tile，执行分割和创建新set的操作
                        self.split_run_and_add_new_set_single(river, group, tile, potential_set)
                        suits_needed.remove(tile.suit)
                        potential_set.append(tile)
                        if len(potential_set) == 3:
                            return True  # 已经组成一个set
            # 检查4张牌的sets
            if len(group) == 4 and self.is_set(group):
                for tile in group:
                    if tile.number == potential_set[0].number and tile.suit in suits_needed:
                        potential_set.append(tile)
                        suits_needed.remove(tile.suit)
                        if len(potential_set) == 3:
                            return True
        return False

    def remove_tile_from_river(self, game, tile):
        for group in game.river:
            if tile in group:
                group.remove(tile)
                if not group:  # 如果组合为空，从river中完全移除
                    game.river.remove(group)
                break

    def split_run_and_add_new_set_single(self, river, run, tile_to_remove, potential_set):
        """将run从tile_to_remove处分开，并创建新的set"""
        index = run.index(tile_to_remove)
        left_part = run[:index]  # 获取tile左侧的部分
        right_part = run[index + 1:]  # 获取tile右侧的部分

        # 只有当左右部分仍然是有效的run时，才进行分割
        if len(left_part) >= 3:
            river.append(left_part)
        if len(right_part) >= 3:
            river.append(right_part)

        river.remove(run)  # 从river中移除原来的run

        # 从手牌中移除用于新set的tiles
        new_set = [tile for tile in potential_set]
        for tile in new_set:
            if tile in self.hand:
                self.hand.remove(tile)

        river.append(new_set)  # 将新set加入到river
        self.print(f"{self.name} split run at {tile_to_remove} and created new set {new_set}")

    def has_won(self):
        return not self.hand  # Player wins if hand is empty

    def simulate_cold_start(self, game):
        """
        Check if a player can pass the cold_start_rule, if yes, play the tiles and print it passes the cold start rule.
        :param game: 
        :return: 
        """
        if self.has_met_cold_start:
            return
        original_hand = self.hand[:]
        temporary_river = []
        while True:
            melds = self.find_melds(original_hand)
            if not melds:
                break
            best_meld = max(melds, key=lambda m: sum(tile.number for tile in m))
            for tile in best_meld:
                original_hand.remove(tile)  # Remove from temporary hand
            temporary_river.append(best_meld)
        # Check if the total points of melds in temporary river meet the requirement
        if sum(tile.number for meld in temporary_river for tile in meld) >= 30:
            self.has_met_cold_start = True
            if not any(p.is_first_cold_start for p in game.players): ###
                self.is_first_cold_start = True
            for meld in temporary_river:
                self.play_tiles(meld, game)
            self.hand = original_hand  
            self.print(f"{self.name} has passed the cold start rule.")
        # else:
            # self.hand = original_hand  

class Game:
    def __init__(self, players, strategies=None, cold_start_enabled=True, verbose=False):
        self.verbose = verbose  # 控制打印输出, put in the first!
        self.deck = Deck() # shuffle
        self.players = [Player(name, game=self) for name in players]
        self.strategies = strategies  # Store strategies if provided
        self.initialize_game()
        self.river = []  # 存放所有玩家打出的牌
        self.cold_start_enabled = cold_start_enabled  # 控制是否啟用cold_start規則
        self.first_cold_start_player = None  # To track the first player who meets the cold start
        self.tempt_river = []
        self.tempt_hand = []
        self.total_points = 0



    def print(self, message):
        """Utility method to control print statements based on verbosity."""
        if self.verbose:
            print(message)

    def initialize_game(self):
        for player in self.players:
            player.draw_tiles(self.deck, 14)
            player.reset_stats()
            self.print(f"{player.name}'s starting hand: {[str(tile) for tile in player.hand]}")
            # Print remaining number of cards in the deck after initial drawing:
        self.print(f"Remaining tiles in deck: {len(self.deck.tiles)}")

    def play_round(self):
        round = 0
        if self.first_cold_start_player is None:
            for player in self.players:
                if player.is_first_cold_start:
                    self.first_cold_start_player = player.name
                    break
        while True:
            round += 1
            self.print(f"Round {round}")
            for player in self.players:
                self.player_turn(player)
                if not player.hand:  # 检查玩家手牌是否为空
                    self.print(f"{player.name} wins with an empty hand!")
                    return player.name
            if not self.deck.tiles:  # 检查牌堆是否已空
                self.print("Deck is empty, game over.")
                return self.determine_winner_when_deck_empty()  # "Game ended because the deck is empty."

    def determine_winner_when_deck_empty(self):
        # Find the minimum hand size
        min_hand_size = min(len(player.hand) for player in self.players)
        # Filter players with the minimum hand size
        candidates = [player for player in self.players if len(player.hand) == min_hand_size]

        if len(candidates) == 1:
            self.print(f"{candidates[0].name} wins by having the fewest tiles!")
            return [candidates[0].name]  # Only one player has the minimum hand size

        # If more than one candidate, compare the sum of numbers in their hands
        min_hand_sum = min(sum(tile.number for tile in player.hand) for player in candidates)
        winners = [player.name for player in candidates if sum(tile.number for tile in player.hand) == min_hand_sum]

        self.print(f"Players {', '.join(winners)} win by having the fewest tiles with the lowest sum of numbers!")
        return winners  # Return all winning players if tied

    def player_turn(self, player):
        self.print(f"{player.name}'s turn:")
        if self.cold_start_enabled and not player.has_met_cold_start:
            player.simulate_cold_start(self)
            if player.is_first_cold_start:
                self.print(f"{player.name} is the first to pass the cold start.")
            if not player.has_met_cold_start:  # If still not met, draw tiles
                player.draw_tiles(self.deck, 1)
                self.print(f"{player.name} drew 1 tile because no valid melds meet the cold start condition")
                # self.print_river()
        else:
            melds_played = 0
            while True:
                any_action_taken = False

                melds = player.find_melds()
                if melds:
                    best_meld = max(melds, key=lambda m: sum(tile.number for tile in m))
                    player.play_tiles(best_meld, self)
                    melds_played += 1
                    any_action_taken = True

                extendable_set = player.find_sets_match_in_hand_and_river(self.river)
                if extendable_set:
                    player.extendable_set_play_tiles(self, extendable_set)
                    melds_played += 1
                    any_action_taken = True

                extendable_run = player.find_runs_match_in_hand_and_river(self.river)
                if extendable_run:
                    player.extend_run_play_tiles(extendable_run, self.river)
                    melds_played += 1
                    any_action_taken = True

                insert_or_not = player.insert_and_split_runs(self.river, self)
                if insert_or_not:
                    melds_played += 1
                    any_action_taken = True

                pair_or_not = player.find_and_modify_runs_or_sets(self)
                if pair_or_not:
                    melds_played += 1
                    any_action_taken = True

                single_set = player.find_single_set(self)
                if single_set:
                    melds_played += 1
                    any_action_taken = True

                if not any_action_taken:
                    break

            if melds_played == 0:
                player.draw_tiles(self.deck, 1)
                # self.print_river()

        self.print(f"{player.name}'s turn ends.")  # Adjusted to dot notation
        self.print(
            f"{player.name}'s hand after the round: {[f'{tile.suit[0]}{tile.number}' for tile in player.hand]}")  # Adjusted to dot notation

        return {player.name: 'win' for player in self.players}

    def update_river(self, meld):
        self.river.append(meld)
        self.print(f"Updated River: {self.river}")

    def print_river(self):
        self.print(f"Current River: {self.river}")

    def conclude_game(self):
        winners = [player for player in self.players if player.has_won()]
        if len(winners) == 1:  # Assuming exactly one winner per game
            winner = winners[0]
            winner.wins += 1
            for player in self.players:
                if player != winner:
                    player.losses += 1
        else:
            # Handle ties or no winners scenario if applicable
            for player in self.players:
                player.ties += 1  # or adjust based on your game's rules

def monte_carlo_simulation(num_games, players):
    results = {'total': 0}
    player_stats = {player: {'wins': 0, 'losses': 0, 'ties': 0} for player in players}
    cold_start_stats = {player: {'wins': 0, 'losses': 0, 'ties': 0} for player in players}

    for _ in range(num_games):
        game = Game(players, verbose=False)
        winners = game.play_round()
        for player in game.players:
            if player.name in winners:
                player_stats[player.name]['wins'] += 1
            else:
                player_stats[player.name]['losses'] += 1

            if player.is_first_cold_start:
                if player.name in winners:
                    cold_start_stats[player.name]['wins'] += 1
                else:
                    cold_start_stats[player.name]['losses'] += 1

    return results, player_stats, cold_start_stats

def display_statistics(results, player_stats, first_cold_start_stats):
    print("Starting Rummikub Games.\n")
    print("-" * 65)
    print("\nTournament Player Statistics:\n")
    print("Name             Win%      Won       Lost")
    print("-------------- ------ ----------- ----------")

    for player, stats in player_stats.items():
        win_percent = (stats['wins'] / (stats['wins'] + stats['losses'])) * 100 if stats['wins'] + stats['losses'] > 0 else 0
        print(f"{player:15} {win_percent:6.2f}% {stats['wins']:10d} {stats['losses']:10d}")

    print("\nFirst Cold_Start Winning States\n")
    print("Name                             Win%      Won       Lost")
    print("------------------------------ ------ ----------- ----------")

    total_first_cold_wins = 0
    total_first_cold_losses = 0

    for player, stats in first_cold_start_stats.items():
        win_percent = (stats['wins'] / (stats['wins'] + stats['losses'])) * 100 if stats['wins'] + stats['losses'] > 0 else 0
        print(f"{player:30} {win_percent:6.2f}% {stats['wins']:10d} {stats['losses']:10d}")
        total_first_cold_wins += stats['wins']
        total_first_cold_losses += stats['losses']
    print("------------------------------ ------ ----------- ----------")
    total_games = total_first_cold_wins + total_first_cold_losses
    aggregate_win_percent = (total_first_cold_wins / total_games) * 100 if total_games > 0 else 0
    average_not_first_win = total_first_cold_losses/3
    average_not_first_lost = total_games - average_not_first_win
    average_not_first_win_percent = (average_not_first_win / total_games) * 100 if total_games > 0 else 0

    print(f"\nAggregate first_cold_start    {aggregate_win_percent:6.2f}% {total_first_cold_wins:10d} {total_first_cold_losses:10d}")
    print(f"Average not_first_cold_start  {average_not_first_win_percent:6.2f}% {average_not_first_win:10.0f} {average_not_first_lost:10.0f}\n")


if __name__ == '__main__':
    number_games = 10000
    results, player_stats, first_cold_start_stats = monte_carlo_simulation(number_games, ["Winni", "Peter", "Rachel", "Carol"])
    display_statistics(results, player_stats, first_cold_start_stats)




