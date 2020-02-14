# 👨‍🎨 YThemeCreator

 つ ◕_◕ つ Theme creator for more [DarkCode](https://marketplace.visualstudio.com/items?itemName=yedhrab.darkcode-theme-adopted-python-and-markdown) themes

## 👨‍💻 Usage

- ⚙️ Modify `settings.json` file to generate more themes
- 💫 Than just use `main.py` to generate new themes

## 🕰️ Deprecated Usage

- 💫 Use `color_handler.py` to invert color
- 📦 Install dependencies `npm install` for use `invert_color.js` (optional)

## 🎨 Color Structure

- 🏗️ Default structure of naming `<colorName><darkerValue><shadowValue>`
- ⭐ if yellow equals `ffc000` yellowS2 will equal `ffc000aa`

### 🌁 Shadow Values

| Endfix | Value |
| -  |  - |
| `S1` | `ee` |
| `S2` | `aa` |
| `S3` | `77` |
| `S4` | `55` |
| `S5` | `33` |
| `S6` | `11` |
| `S0` | `00` |

### 🌃 Darker Values

| Endfix | Value |
| -  |  - |
| `D1` | One level darker |
| `D2` | Two level darker |
| `D*` | `*` level darker |
| `D0` | Completely darker |

## ⭐ `settings.json` Example

🖤 DarkCode Theme is well known example for usage.

```json
{
	"coreTheme": "./darkcode.json",
	"outputDir": "../themes",
	"extensions": [
		{
			"postname": "+",
			"postfix": "-plus",
			"options": {
				"editorSuggestWidget.border": "#413701",
				"editorSuggestWidget.foreground": "#bb8b12",
				"editorSuggestWidget.highlightForeground": "#ffbf40b4",
				"editorSuggestWidget.selectedBackground": "#41370177",
				"tab.activeBorderTop": "#FFC000",
				"tab.hoverBackground": "#FFC00010",
				"tab.hoverBorder": "#ffd90070"
			}
		},
		{
			"postname": "++",
			"postfix": "-plus-plus",
			"options": {
				"editorSuggestWidget.border": "#413701",
				"editorSuggestWidget.foreground": "#bb8b12",
				"editorSuggestWidget.highlightForeground": "#ffbf40b4",
				"editorSuggestWidget.selectedBackground": "#41370177",
				"tab.activeBorderTop": "#FFC000",
				"tab.hoverBackground": "#FFC00010",
				"tab.hoverBorder": "#ffd90070",
				"editorHoverWidget.foreground": "#bb8b12",
				"menu.foreground": "#bb8b12",
				"titleBar.activeForeground": "#bb8b12"
			}
		}
	],
	"themes": [
		{
			"name": "DarkCode Contrast",
			"colors": {
				"#1c2022": "#000000",
				"#252b2e": "#161616",
				"#171a1b": "#0a0c0c",
				"#111518": "#181717",
				"#374140": "#24211e",
				"#22212b": "#191824",
				"#eeeeee": "#ffffff",
				"#C0C0C0": "#acacaa",
				"#333333": "#1f1f1f",
				"#cecece": "#e7e7e7",
				"#6b4101": "#aa6600",
				"#413701": "#411e01",
				"#ad550d": "#ad550d",
				"#ececec": "#ececec",
				"#bababa": "#bababa",
				"#ffc000": "#ffc000",
				"#bb8b12": "#bb8b12"
			}
		}
	]
}

```

## 🐞 Known Bug

- 🙄 Inverting doesnt act well


## 💖 Destek ve İletişim

​[​![Github](../.github/assets/github_32px.png)​](https://github.com/yedhrab) [​![LinkedIn](../.github/assets/linkedin_32px.png)​](https://www.linkedin.com/in/yemreak/) [​![Website](../.github/assets/geography_32px.png)​](https://yemreak.com/) [​![Mail](../.github/assets/gmail_32px.png)​](mailto:yemreak.com@gmail.com?subject=YThemeCreator%20%7C%20GitHub)​

​[​![Patreon](../.github/assets/become_a_patron_32px.png)](https://www.patreon.com/yemreak/)

## 🔏 Lisans

**The** [**Apache 2.0 License**](https://choosealicense.com/licenses/apache-2.0/) **©️ Yunus Emre Ak**

![YEmreAk](../.github/assets/ysigniture-trans.png)
