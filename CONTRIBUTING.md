# Contributing

Heya, firstly thanks for helping out! Feel free to add to the library your own music or ones online with the right attribution. Please guys I don't want to be sued u_u

## Suggest music

[Open an issue](https://github.com/Writality/music-library/issues/new) with a link to the track or album, the artist's name, and which collection you think it fits. Tell me what you like about it too, if you want.

If you know where the artist explains how their music can be used, drop that link in as well. Free to listen does not always mean I can host the audio, so I'll check the terms before adding anything. If it's your own music, let me know how you'd like to be credited and whether I can host it.

Some sources need a login or checkout. That's fine, just send the link. A couple of those are already listed in [ATTRIBUTION.md](ATTRIBUTION.md).

## Send a pull request

You can also add music directly. Put the MP3 in `tracks/<collection>/`, then add an entry like this to `manifest.json` (remove the comments before saving; JSON does not allow them):

```jsonc
{
  "id": 2030, // Pick an unused positive integer for this library's track.
  "file": "tracks/lo-fi/30.mp3",
  "title": "Track title",
  "artist": "Artist name",
  "sourceUrl": "https://example.com/original-track",
  "license": "CC BY 4.0",
  "licenseUrl": "https://creativecommons.org/licenses/by/4.0/",
  "attribution": "Track title by Artist name",
  "changes": "Original file; no changes." // Describe edits here if you modified the audio.
}
```

Add the ID to the appropriate collection's `tracks` list. For a new collection, add its `id`, `title`, `description`, `imageOriginal`, `image`, image credits, and track IDs to `collections` too. Collection IDs use lowercase letters, numbers, and hyphens.

Each collection has its own image directory, `images/<collection-id>/`. Put a PNG, JPEG, WebP, or AVIF original there and set `imageOriginal` to its path, for example `"images/lo-fi/cover.jpg"`. Set `image` to the corresponding small JPEG path, for example `"images/lo-fi/cover-small.jpg"`. The manifest updater creates that image at up to 1024 pixels on its longest side; Writality should load `image`. Set both fields to `null` while artwork is pending. Add `imageAttribution` (for example, `Photo by Name on Unsplash`), `imageCreatorUrl`, and `imageSourceUrl` so the app can show credit and link to the photographer and original photo. Also record the credit and usage terms in [ATTRIBUTION.md](ATTRIBUTION.md).

The job on `main` fills in `duration`, `sizeBytes`, and `sha256` and generates smaller images after the pull request is merged. Leave generated track fields out of new entries. You can run `python3 scripts/update_manifest.py` locally if you have FFmpeg installed.

Not every track has a published license. Use the fields to describe the actual rights, without inventing a Creative Commons license:

- `license`: put the published license or rights status. If the rights holder gave Writality direct permission, use `Used with permission` and explain the permitted use in the pull request.
- `licenseUrl`: link to published terms or a public permission statement when available. Use `N/A` if there is no public link, and explain the permission in the pull request so it can be reviewed case by case. Do not invent a URL.
- `sourceUrl`: link to the artist's original page. For an unpublished track, link to the pull request where the artist submitted the original file.
- `attribution`: write the credit the artist requested. `changes` records edits to the audio, such as trimming or converting it; use `Original file; no changes.` if there were none.

I review permission to host and distribute the audio before merging. If permission is unclear, or you cannot provide the audio, open an issue or send a pull request with the source and rights information in [ATTRIBUTION.md](ATTRIBUTION.md); I can add the file after the rights are settled.

Found a wrong title, credit, or broken link? Open an issue or send a pull request.
