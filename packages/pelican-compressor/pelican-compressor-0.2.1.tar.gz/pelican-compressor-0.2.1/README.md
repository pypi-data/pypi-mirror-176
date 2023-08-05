# Pelican plugin for [`web-compressor`](https://codeberg.org/digitalbuero/web-compressor)

`pelican-compress` optimizes any Pelican site's `output` - using sane defaults & insane tools.


## Installation

It's available from [PyPi](https://pypi.org/project/pelican-compressor) using a package manager of your choice:

```text
# Using 'pip'
pip install pelican-compressor

# Using 'poetry'
poetry add pelican-compressor
```


## Getting started

Using `pelican-compressor` is straightforward:


### Plugin

After installing it, the following features are enabled by default:
- minification of HTML files & web assets, such as CSS/JS, JSON & XML files
- cachebusting assets, such as CSS/JS, JSON & XML files, fonts and images
- creating SRI hashes for `link` & `script` tags

See 'Configuration' below for full control over these processes and even more features, such as
- optimizing all JPEG & PNG images
- converting them to modern file formats such as AVIF/WebP
- building CSP directives (including nonces for inline scripts & styles)


### Commandline

Installing `pelican-compressor` also gives you access to [`webcompr`](https://codeberg.org/digitalbuero/web-compressor), which might be interesting for more flexibility.


## Configuration

The following settings need to be prepended by `COMPRESSOR_` to work, eg for enabling AVIF/WebP generation, define `COMPRESSOR_ENABLE_MODERN_FORMATS = True` [in your settings](https://docs.getpelican.com/en/latest/settings.html#settings) (most likely `pelicanconf.py`).


### General

| Setting      | Type   | Default | Description              |
| ------------ | ------ | ------- | ------------------------ |
| `BLOCK_LIST` | `list` | `[]`    | Filenames to be excluded |


### Asset minification

| Setting             | Type                   | Default            | Description              |
| ------------------- | ---------------------- | ------------------ | ------------------------ |
| `ENABLE_MINIFY`     | `bool`                 | `true`             | Enables/disables feature |
| `MINIFY_MEDIATYPES` | `list` or `re.Pattern` | HTML, CSS, JS, SVG | Files to be minified     |
| `MINIFY_OPTIONS`    | `dict`                 | see below          | Minification settings    |

For available minification settings, see [here](https://github.com/tdewolff/minify/tree/master/bindings/py#usage).


### Image optimizations

| Setting                 | Type                   | Default | Description                |
| ----------------------- | ---------------------- | ------- | -------------------------- |
| `ENABLE_IMAGEOPTIM`     | `bool`                 | `false` | Enables/disables feature   |
| `IMAGEOPTIM_MEDIATYPES` | `list` or `re.Pattern` | JPG/PNG | Files to be optimized      |
| `JPEG_QUALITY`          | `int`                  | `85`    | JPEG output quality        |
| `STRIP_METADATA`        | `bool`                 | `true`  | Whether to remove metadata |


### Asset hashing / "cachebusting"

| Setting            | Type                   | Default                      | Description                         |
| ------------------ | ---------------------- | ---------------------------- | ----------------------------------- |
`ENABLE_HASHING`     | `bool`                 | `true`                       | Enables/disables feature            |
`HASHING_MEDIATYPES` | `list` or `re.Pattern` | CSS/JS files, fonts & images | Files to be hashed                  |
`HASH_LENGTH`        | `int`                  | `10`                         | Length of appended hash string      |
`HASH_MODIFIED`      | `bool`                 | `false`                      | Hash modified time or file contents |


### AVIF / WebP generation

| Setting               | Type   | Default           | Description               |
| --------------------- | ------ | ----------------- | ------------------------- |
`ENABLE_MODERN_FORMATS` | `bool` | `false`           | Enables/disables feature  |
`AVIF_SETTINGS`         | `dict` | `{"quality": 90}` | AVIF settings (see below) |
`WEBP_SETTINGS`         | `dict` | `{"method": 6}`   | WebP settings (see below) |

Available WebP settings:
- `lossless`
- `quality`
- `method`
- `icc_profile`
- `exif`

For more information, see [`Pillow` docs](https://pillow.readthedocs.io/en/stable/handbook/image-file-formats.html?highlight=webp#webp).

Available AVIF settings:
- `advanced`
- `alpha_premultiplied`
- `append_images`
- `codec`
- `duration`
- `exif`
- `icc_profile`
- `qmax`
- `qmin`
- `quality`
- `range`
- `speed`
- `subsampling`
- `tile_rows`
- `xmp` / `XML:com.adobe.xmp`

**Note**: AVIF generation is provided through a plugin, which [hasn't made it into `Pillow`'s core yet](https://github.com/python-pillow/Pillow/pull/5201), so consider this feature as being experimental!

For more information (eg default values), check out the `info.get()` calls inside the `_save()` method, courtesy of the [`pillow_avif` plugin](https://github.com/fdintino/pillow-avif-plugin/blob/master/src/pillow_avif/AvifImagePlugin.py#L114).


### Subresource integrity

| Setting    | Type  | Default    | Description                 |
| ---------- | ----- | ---------- | --------------------------- |
`ENABLE_SRI` | `str` | `true`     | Enables/disables feature    |
`SRI_DIGEST` | `str` | `'sha512'` | Cryptographic digest to use |


### Content security policy

| Setting        | Type   | Default            | Description                 |
| -------------- | ------ | ------------------ | --------------------------- |
`ENABLE_CSP`     | `bool` | `false`            | Enables/disables feature    |
`CSP_DIGEST`     | `str`  | `'sha512'`         | Cryptographic digest to use |
`CSP_NONCE`      | `str`  | `uuid.uuid4().hex` | Random nonce to be used     |
`CSP_DIRECTIVES` | `dict` | `{}`               | CSP directives (see below)  |

When creating a [content security policy](https://www.w3.org/TR/CSP3), you might want to start with something restrictive and go from there:

```python
COMPRESSOR_ENABLE_CSP = True
COMPRESSOR_CSP_DIRECTIVES = {
    "default-src": "none",
    "script-src": "'strict-dynamic'",
    "object-src": "none",
    "base-uri": "none",
},
```


### Hooks

It's also prossible to assign functions to be called right before this plugin (`PRE_HOOK`) or immediately thereafter (`POST_HOOK`), eg for creating image variants (such as placeholders for lazyloading). Each function receives the argument `asset`, which is a tuple consisting of the `pathlib.Path` to each asset file and a `str` representing its MIME type:

```python
# pelicanconf.py

COMPRESSOR_PRE_HOOK = lambda asset: (
    # Unpack asset file & mediatype
    file_path, mime_type = asset

    # If image file ..
    if mime_type == "image/jpeg":
        # .. do something
)
```


## Roadmap

- [x] Update `README.md`
- [ ] Add tests
