from common.Settings import Settings

comment_settings = Settings.Comment(
    header="<details><summary>:robot: Hey, I'm @LmmsBot from github.com/lmms/bot "
           "and I made downloads for this pull request!</summary><p>\n"
           "\n",
    footer="</p></details>\n"
           "\n",
    download_line="- {title.title} {title.platform_name}: [{download_link.basename}]({download_link}) ([build link]("
                  "build_link))\n",
    json_header='<details><summary>:robot:</summary>\n'
                '\n'
                '```json\n',
    json_footer='\n'
                '```\n'
                '</details>',
    section_title='## {platform_title}\n'
)

github_settings = Settings.Github(
    username="<username>",
    token='<token>',
)

linux = Settings.Platform(
    name="Linux",
    extension_to_title={
        "AppImage": "(AppImage)",
    }
)

windows = Settings.Platform(
    name="Windows",
    extension_to_title={
        'mingw.win32.exe': "32-bit (mingw)",
        'mingw.win64.exe': "64-bit (mingw)",
        'msvc17.win32.exe': "32-bit (MSVC 2017)",
        'msvc17.win64.exe': "64-bit (MSVC 2017)",
    }
)

macOS = Settings.Platform(
    name="macOS",
    extension_to_title={
        "dmg": ""
    }
)

settings = Settings(
    comment=comment_settings,
    github=github_settings,
    platforms=(linux, windows, macOS)
)
