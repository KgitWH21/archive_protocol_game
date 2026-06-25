import random
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich import box

console = Console()

class Card:
    def __init__(self, name, energy, damage=0, block=0, burn=0, vulnerable=0):
        self.name = name
        self.energy = energy
        self.damage = damage
        self.block = block
        self.burn = burn
        self.vulnerable = vulnerable

class Player:
    def __init__(self, name):
        self.name = name
        self.max_hp = 50
        self.hp = 50
        self.block = 0
        self.energy = 3
        self.deck = [
            Card("CQB Strike", 1, damage=8),
            Card("CQB Strike", 1, damage=8),
            Card("Suppressive Fire", 2, damage=14),
            Card("Stealth Protocol", 1, block=10),
            Card("Temporal Resonance", 2, block=5, damage=5)
        ]
        self.discard = []
        random.shuffle(self.deck)

    def _reshuffle(self):
        console.print("[dim][System] Reshuffling discard pile into deck...[/dim]\n")
        self.deck = self.discard[:]
        self.discard = []
        random.shuffle(self.deck)

    def draw_hand(self, size=3):
        hand = []
        for _ in range(size):
            if not self.deck:
                if not self.discard:
                    break
                self._reshuffle()
            hand.append(self.deck.pop())
        return hand

class Enemy:
    def __init__(self, name, hp, min_atk, max_atk):
        self.name = name
        self.hp = hp
        self.min_atk = min_atk
        self.max_atk = max_atk
        self.intent = 0
        self.burn = 0
        self.vulnerable = 0

    def roll_intent(self):
        self.intent = random.randint(self.min_atk, self.max_atk)

    def attack(self):
        return self.intent

    def tick_status(self):
        if self.burn > 0:
            console.print(f"[red]> {self.name} takes {self.burn} burn damage![/red]")
            self.hp -= self.burn
            self.burn -= 1
        if self.vulnerable > 0:
            self.vulnerable -= 1
            if self.vulnerable == 0:
                console.print(f"[dim]> {self.name} is no longer Vulnerable.[/dim]")

REWARD_POOL = [
    Card("Frag Grenade",       2, damage=18),
    Card("Neural Disruptor",   2, damage=10, block=5),
    Card("Ghost Step",         1, block=15),
    Card("Overcharge",         3, damage=25),
    Card("Reactive Armor",     2, block=12),
    Card("Tactical Reload",    0, damage=4,  block=4),
    Card("Cipher Blade",       1, damage=11),
    Card("EMP Burst",          2, damage=12, block=6),
    Card("Dead Drop",          1, block=8),
    Card("Kinetic Surge",      3, damage=20, block=8),
    Card("Incendiary Round",   2, damage=6,  burn=4),
    Card("Marked Target",      1, damage=4,  vulnerable=2),
    Card("Napalm Protocol",    3, damage=10, burn=6),
    Card("Exploit Weakness",   2, vulnerable=3),
]

ENCOUNTERS = [
    Enemy("Awakened Cultist",      hp=30, min_atk=4,  max_atk=9),
    Enemy("Archive Sentinel",      hp=45, min_atk=6,  max_atk=13),
    Enemy("Okinawa Core Fragment", hp=65, min_atk=8,  max_atk=18),
]


def status_tags(enemy):
    tags = []
    if enemy.burn > 0:
        tags.append(f"[red]Burn {enemy.burn}[/red]")
    if enemy.vulnerable > 0:
        tags.append(f"[magenta]Vulnerable {enemy.vulnerable}[/magenta]")
    return "  ".join(tags) if tags else "[dim]none[/dim]"


def render_status(player, enemy, turn):
    hp_color = "green" if player.hp > player.max_hp * 0.5 else "yellow" if player.hp > player.max_hp * 0.25 else "red"
    player_panel = Panel(
        f"[{hp_color}]HP: {player.hp}/{player.max_hp}[/{hp_color}]\n"
        f"[cyan]Block: {player.block}[/cyan]  [yellow]Energy: {player.energy}[/yellow]",
        title=f"[bold white]{player.name}[/bold white]",
        border_style="cyan",
    )
    enemy_hp_color = "green" if enemy.hp > 30 else "yellow" if enemy.hp > 15 else "red"
    intent_color = "red" if enemy.intent >= 10 else "yellow"
    enemy_panel = Panel(
        f"[{enemy_hp_color}]HP: {enemy.hp}[/{enemy_hp_color}]\n"
        f"[{intent_color}]INTENT: Strike for {enemy.intent} dmg[/{intent_color}]\n"
        f"Status: {status_tags(enemy)}",
        title=f"[bold red]{enemy.name}[/bold red]",
        border_style="red",
    )
    console.print(f"\n[bold]TURN {turn}[/bold]")
    console.print(Columns([player_panel, enemy_panel]))


def render_deck(player, hand):
    def card_table(cards, title, border):
        table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta")
        table.add_column("Card", style="bold white")
        table.add_column("Cost", justify="center", style="yellow")
        table.add_column("DMG",  justify="center", style="red")
        table.add_column("BLK",  justify="center", style="cyan")
        table.add_column("Burn", justify="center", style="red")
        table.add_column("Vuln", justify="center", style="magenta")
        for card in cards:
            table.add_row(
                card.name,
                str(card.energy),
                str(card.damage)     if card.damage     else "—",
                str(card.block)      if card.block      else "—",
                str(card.burn)       if card.burn       else "—",
                str(card.vulnerable) if card.vulnerable else "—",
            )
        return Panel(table, title=title, border_style=border)

    console.print(card_table(player.deck,    f"[bold]Deck ({len(player.deck)} cards)[/bold]",    "cyan"))
    console.print(card_table(hand,           f"[bold]Hand ({len(hand)} cards)[/bold]",            "white"))
    console.print(card_table(player.discard, f"[bold]Discard ({len(player.discard)} cards)[/bold]", "dim"))


def render_hand(hand):
    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta")
    table.add_column("#",    style="dim",  width=3)
    table.add_column("Card", style="bold white")
    table.add_column("Cost", justify="center", style="yellow")
    table.add_column("DMG",  justify="center", style="red")
    table.add_column("BLK",  justify="center", style="cyan")
    table.add_column("Burn", justify="center", style="red")
    table.add_column("Vuln", justify="center", style="magenta")
    for i, card in enumerate(hand):
        table.add_row(
            str(i + 1),
            card.name,
            str(card.energy),
            str(card.damage)     if card.damage     else "—",
            str(card.block)      if card.block      else "—",
            str(card.burn)       if card.burn       else "—",
            str(card.vulnerable) if card.vulnerable else "—",
        )
    console.print(Panel(table, title="[bold]Your Hand[/bold]", border_style="dim white"))
    console.print("  [dim][0] End Turn  [d] View Deck[/dim]")


def offer_card_reward(player):
    choices = random.sample(REWARD_POOL, 3)
    console.print(Panel(
        "[bold yellow]Data fragment recovered.[/bold yellow]\nChoose a card to add to your deck:",
        border_style="yellow"
    ))

    table = Table(box=box.SIMPLE_HEAVY, show_header=True, header_style="bold magenta")
    table.add_column("#",    style="dim",  width=3)
    table.add_column("Card", style="bold white")
    table.add_column("Cost", justify="center", style="yellow")
    table.add_column("DMG",  justify="center", style="red")
    table.add_column("BLK",  justify="center", style="cyan")
    table.add_column("Burn", justify="center", style="red")
    table.add_column("Vuln", justify="center", style="magenta")
    for i, card in enumerate(choices):
        table.add_row(
            str(i + 1),
            card.name,
            str(card.energy),
            str(card.damage)     if card.damage     else "—",
            str(card.block)      if card.block      else "—",
            str(card.burn)       if card.burn       else "—",
            str(card.vulnerable) if card.vulnerable else "—",
        )
    console.print(table)
    console.print("  [dim][0] Skip[/dim]\n")

    while True:
        pick = input("Your choice: ").strip()
        if pick == '0':
            console.print("[dim][System] Card reward skipped.[/dim]\n")
            return
        try:
            idx = int(pick) - 1
            if 0 <= idx < len(choices):
                gained = choices[idx]
                player.discard.append(gained)
                console.print(f"\n[green][System] [bold]{gained.name}[/bold] added to your deck.[/green]\n")
                return
            else:
                console.print("[red][!] Invalid selection.[/red]\n")
        except ValueError:
            console.print("[red][!] Please enter a number.[/red]\n")


def offer_rest_or_scavenge(player):
    console.print(Panel(
        f"[bold]Choose your next action:[/bold]\n\n"
        f"[green][1] REST[/green]       Recover 15 HP  [dim](Current: {player.hp}/{player.max_hp})[/dim]\n"
        f"[yellow][2] SCAVENGE[/yellow]    Add a card to your deck",
        border_style="dim",
        title="[bold]Between Sectors[/bold]"
    ))

    while True:
        pick = input("Your choice: ").strip()
        if pick == '1':
            heal = 15
            player.hp = min(player.max_hp, player.hp + heal)
            console.print(f"\n[green][System] Rested. Recovered {heal} HP. Current HP: {player.hp}/{player.max_hp}[/green]\n")
            return
        elif pick == '2':
            offer_card_reward(player)
            return
        else:
            console.print("[red][!] Enter 1 or 2.[/red]\n")


def run_combat(player, enemy):
    console.print(Panel(
        f"[bold red]WARNING:[/bold red] [white]{enemy.name}[/white] detected in the sector.",
        border_style="red"
    ))
    time.sleep(1)

    enemy.roll_intent()
    turn = 1
    while player.hp > 0 and enemy.hp > 0:
        render_status(player, enemy, turn)
        hand = player.draw_hand()

        while player.energy > 0 and enemy.hp > 0:
            render_hand(hand)
            choice = input("\nSelect a card to play: ").strip().lower()

            if choice == '0':
                break

            if choice == 'd':
                render_deck(player, hand)
                continue

            try:
                card_index = int(choice) - 1
                if 0 <= card_index < len(hand):
                    played_card = hand[card_index]

                    if player.energy >= played_card.energy:
                        player.energy -= played_card.energy
                        player.block += played_card.block

                        dmg = played_card.damage
                        if dmg > 0 and enemy.vulnerable > 0:
                            dmg = int(dmg * 1.5)

                        enemy.hp -= dmg
                        enemy.burn += played_card.burn
                        enemy.vulnerable += played_card.vulnerable

                        console.print(f"\n[bold yellow]> You played {played_card.name}![/bold yellow]")
                        if dmg > 0:
                            bonus = " [magenta](+50% Vulnerable!)[/magenta]" if played_card.damage > 0 and enemy.vulnerable > 0 else ""
                            console.print(f"[red]> Dealt {dmg} damage to {enemy.name}.{bonus}[/red]")
                        if played_card.block > 0:
                            console.print(f"[cyan]> Gained {played_card.block} block.[/cyan]")
                        if played_card.burn > 0:
                            console.print(f"[red]> Applied Burn {played_card.burn} to {enemy.name}.[/red]")
                        if played_card.vulnerable > 0:
                            console.print(f"[magenta]> Applied Vulnerable {played_card.vulnerable} to {enemy.name}.[/magenta]")
                        console.print()

                        player.discard.append(hand.pop(card_index))
                    else:
                        console.print("[red][!] Not enough energy.[/red]\n")
                else:
                    console.print("[red][!] Invalid selection.[/red]\n")
            except ValueError:
                console.print("[red][!] Please enter a number.[/red]\n")

        player.discard.extend(hand)
        hand.clear()

        if enemy.hp > 0:
            console.print(f"\n[bold red]--- {enemy.name}'s Turn ---[/bold red]")
            time.sleep(1)

            enemy.tick_status()

            if enemy.hp > 0:
                dmg = enemy.attack()
                if player.block >= dmg:
                    player.block -= dmg
                    console.print(f"[cyan]{enemy.name} attacks for {dmg}, but your block absorbed it all![/cyan]\n")
                else:
                    actual_dmg = dmg - player.block
                    player.hp -= actual_dmg
                    player.block = 0
                    console.print(f"[red]{enemy.name} breaks your cover and deals {actual_dmg} damage![/red]\n")

        enemy.roll_intent()
        player.energy = 3
        player.block = 0
        turn += 1
        time.sleep(1)

    return player.hp > 0


def play_game():
    console.print(Panel(
        "[bold cyan]--- INITIATING OKINAWA CONTAINMENT ARCHIVE ---[/bold cyan]\n"
        "[dim]User: Jinhua_Ma // Accessing Simulation Log...[/dim]",
        border_style="cyan",
        box=box.DOUBLE
    ))
    time.sleep(1)

    player = Player("Shade")

    for i, enemy in enumerate(ENCOUNTERS):
        console.rule(f"[bold]SECTOR {i + 1} OF {len(ENCOUNTERS)}[/bold]")

        survived = run_combat(player, enemy)

        if not survived:
            console.print(Panel(
                "[bold red]ARCHIVE CONNECTION LOST.[/bold red]\nJinhua, the simulation failed.",
                border_style="red"
            ))
            return

        console.print(f"\n[bold green]THREAT NEUTRALIZED.[/bold green] {enemy.name} eliminated.\n")

        if i < len(ENCOUNTERS) - 1:
            time.sleep(1)
            offer_rest_or_scavenge(player)

    console.print(Panel(
        "[bold cyan]ALL SECTORS CLEARED.[/bold cyan] The Archive falls silent.\n"
        "[white]You are one step closer to the truth, Jinhua.[/white]",
        border_style="cyan",
        box=box.DOUBLE
    ))


if __name__ == "__main__":
    play_game()
