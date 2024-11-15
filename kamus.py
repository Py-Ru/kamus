import flet as ft
from gtts import gTTS
import io
import pygame


# initialize pygame mixer
pygame.mixer.init()
# test database
hausa_dictionary = {
    "gida": "House or home",
    "aboki": "Friend",
    "mota": "Car",
    "kai": "Head",
    "mace": "Woman",
    "namiji": "Man"
}


def main(page: ft.Page):
    page.title = "Kamus"

    # Boolean to track search mode
    search_mode = False
    # search input
    search_input = ft.TextField(
        hint_text="Search...",
        autofocus=True,
        on_submit=lambda e: search_word(e)
    )
    # result text
    # result_text = ft.Text("Definition will appear here.", size=18)

    # pronunciation button
    pronounce_btn = ft.IconButton(
        ft.icons.VOLUME_UP,
        on_click=lambda e: pronounce_word(search_input.value)
    )

    # Define update_top_bar function
    def update_top_bar(e):
        nonlocal search_mode
        search_mode = not search_mode

        search_input.value = ""

        # Clear the current AppBar content
        page.appbar = None

        # Update AppBar based on search_mode
        if search_mode:
            # Search mode: AppBar with a TextField
            page.appbar = ft.AppBar(
                leading=ft.IconButton(
                    ft.icons.ARROW_BACK, on_click=update_top_bar),
                title=search_input,
                actions=[ft.IconButton(
                    ft.icons.SEARCH, on_click=search_word)],
                bgcolor=ft.colors.BLUE_600
            )
        else:
            # Default mode: AppBar with the title
            page.appbar = ft.AppBar(
                leading=ft.Icon(ft.icons.MENU),
                title=ft.Text("Hausa", weight="bold"),
                actions=[ft.IconButton(
                    ft.icons.SEARCH, on_click=update_top_bar)],
                bgcolor=ft.colors.BLUE_600
            )
        page.update()

    result = ft.Column(
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.START,
        controls=[]
    )

    # vertical menu
    options_list = ft.Column(
        controls=[
            ft.Container(
                on_click=lambda _: on_option_click("Word of the Day"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.TODAY, size=24,
                                color=ft.colors.BLUE_700),
                        ft.Text("Word of the Day", size=18,
                                color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                margin=ft.margin.symmetric(vertical=4),
                border_radius=8,
            ),
            ft.Container(
                on_click=lambda _: on_option_click("History"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.HISTORY, size=24,
                                color=ft.colors.BLUE_700),
                        ft.Text("History", size=18, color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                margin=ft.margin.symmetric(vertical=4),
                border_radius=8,
            ),
            ft.Container(
                on_click=lambda _: on_option_click("Bookmarks"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.BOOKMARK, size=24,
                                color=ft.colors.BLUE_700),
                        ft.Text("Bookmarks", size=18, color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                margin=ft.margin.symmetric(vertical=4),
                border_radius=8,
            ),
            ft.Container(
                on_click=lambda _: on_option_click("Random Word"),
                content=ft.Row(
                    controls=[
                        ft.Icon(ft.icons.SHUFFLE, size=24,
                                color=ft.colors.BLUE_700),
                        ft.Text("Random Word", size=18, color=ft.colors.WHITE)
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                padding=ft.padding.symmetric(horizontal=10, vertical=8),
                margin=ft.margin.symmetric(vertical=4),
                border_radius=8,
            ),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )

    # Initial top bar
    page.appbar = ft.AppBar(
        leading=ft.Icon(ft.icons.MENU),
        title=ft.Text("Hausa", weight="bold"),
        actions=[ft.IconButton(ft.icons.SEARCH, on_click=update_top_bar)],
        bgcolor=ft.colors.BLUE_600
    )

    def toggle_options_list(show_options):
        options_list.visible = show_options
        result.visible = not show_options
        page.update()

    # Title in main content area
    title_text = ft.Text("Hausa", size=24, weight="bold",
                         color=ft.colors.WHITE)

    def search_word(event):
        word = search_input.value.lower()
        if word in hausa_dictionary:
            definition = hausa_dictionary[word]
            result.controls = [
                ft.Row(
                    controls=[
                        ft.Text(f"{word.capitalize()}", size=24,
                                weight="bold", color=ft.colors.WHITE),
                        ft.IconButton(ft.icons.VOLUME_UP,
                                      on_click=lambda _: pronounce_word(word))
                    ],
                    alignment=ft.MainAxisAlignment.START
                ),
                ft.Text(f"Definition: {definition}", size=18)
            ]
            toggle_options_list(False)
        else:
            result.controls = [
                ft.Text(f"'{word}' not found in the dictionary.", size=18)]

        result.update()

    def pronounce_word(word):
        # generate TTS audio
        tts = gTTS(text=word, lang='ha')  # 'ka' is the language code for Hausa
        audio_data = io.BytesIO()
        tts.write_to_fp(audio_data)
        audio_data.seek(0)

        # play audio
        pygame.mixer.music.load(audio_data, 'mp3')
        pygame.mixer.music.play()

    page.add(
        ft.Column(
            controls=[options_list, result],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )
    toggle_options_list(True)  # show options list on load


ft.app(target=main)
