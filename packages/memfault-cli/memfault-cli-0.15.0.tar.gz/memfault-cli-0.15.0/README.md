# Memfault CLI tool

This package contains the `memfault` CLI tool.

The purpose of the tool is to make integration with Memfault from other systems,
like continuous integration servers, as easy as possible.

Install the tool and run `memfault --help` for more info!

## Changes

### 0.15.0

- 💥 Breaking change: update the `upload-yocto-symbols` subcommand to take two
  image paths as required arguments; one for the root filesystem image, and
  another for the debug filesystem image. Versions 0.14.0 and lower used to take
  a guess at the path of the debug filesystem image from the value passed to the
  `--image` param. To avoid confusion and to support all configurations, the
  Memfault CLI no longer does any guessing and now takes two separate params:
  `--image` and `--dbg-image`

### 0.14.0

- ✨ Update the `post-chunk` subcommand to split uploads into batches of 500
  chunks per upload, to avoid timing out when uploading very large chunk logs

### 0.13.0

- 💥 Breaking change: Renamed subcommand `upload-debug-data-recording` to
  `custom-data-recording`

### 0.12.0

- ✨ Added subcommand `upload-debug-data-recording` for uploading debug data
  files

### 0.11.0

- ✨ Enable support for Yocto Dunfell based projects (previously supported
  Kirkstone only)

### 0.10.0

- ✨ Upload-yocto-symbols now uploads additional symbol files

### 0.9.0

- ✨ Expanded support for .elf uploading with the upload-yocto-symbols
  subcommand

### 0.8.0

- ✨ Initial support for upload-yocto-symbols subcommand

### 0.7.0

- 🐛 Updated to correctly only use the GNU build-id `.note` section
