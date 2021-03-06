# XD Theme

Use it if you want `¯\_(ツ)_/¯`

![code](https://user-images.githubusercontent.com/17692058/59829511-3da63b00-9303-11e9-8cb5-f99c29abb81f.png)

<img width="1029" alt="Screen Shot 2019-03-16 at 7 04 13https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-perl-syntax PM" src="https://user-images.githubusercontent.com/17692058/54483273-83dc9180-481e-11e9-99e5-9c8a81a724d3.png">


### Font
- I currently use a customized version of Iosevka: [Here](https://github.com/jeff-hykin/xd-font) 
- You can also use the [Original Iosevka](https://github.com/be5invis/Iosevka) free, open source, and customizable
- The screenshots are using [Input Mono](https://input.fontbureau.com/download/) free, not open source, partially customizable

### Display
It is optimized for a Macbook Pro display.

### Syntax
I use all of the `Better Syntax` extensions, and the Theme is optimized for them
- [Better C++ Syntax](https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-cpp-syntax)
- [Better Dockerfile Syntax](https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-dockerfile-syntax)
- [Better Shell Syntax](https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-shellscript-syntax)
- [Better Perl Syntax](https://marketplace.visualstudio.com/items?itemName=jeff-hykin.better-perl-syntax)

### CSS
I also use custom CSS, which is applied manually. If you want the same CSS, its stored in the `styles.css` file

### Languages
The theme is taylored for
- Javascript + JSX
- C++
- Vue
- JSON
- Python
- Ruby
- Shell
- HTML
- C#
- Dockerfile
- CoffeeScript
- Perl
- CSS
- SASS
- YAML
- Markdown
- WASM
- Cython

### Recommended Settings
```jsonc
{
    "editor.cursorSmoothCaretAnimation" : true,
    "editor.cursorBlinking": "expand",
    "editor.overviewRulerBorder": false,
    "editor.showFoldingControls" :"mouseover",
    "editor.renderWhitespace": "none",
    "editor.fontFamily": "Input Mono, SFMono-UltraLight, SourceCodePro-Light, Menlo, Monaco, 'Courier New', monospace",
    "editor.fontWeight": "200",
    "window.titleBarStyle":"custom",
    "editor.quickSuggestionsDelay": 0,
    // I don't recommend indentRainbow, but if you have it I recommend this:
    "indentRainbow.colors": [
        "rgba(25,59,63,0.4)",
        "rgba(25,44,63,0.4)",
        "rgba(25,25,63,0.4)",
        "rgba(44,25,63,0.4)",
        "rgba(63,25,63,0.4)",
        "rgba(63,25,44,0.4)",
        "rgba(63,44,25,0.4)",
        "rgba(63,63,25,0.4)",
        "rgba(25,63,44,0.4)",
    ],
    "indentRainbow.errorColor": "rgba(128,32,32,0.0)",
}
```

### Caveats
The VS Code setting to "show whitespace" will mess up the underline in python strings

# Setup
Everything is detailed in the `documentation/SETUP.md`!
