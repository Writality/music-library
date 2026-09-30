# Contributing

Heya, firstly thanks for helping out! Feel free to add to the library your own music or ones online with the right attribution. Please guys I don't want to be sued u_u

## Suggest music

[Open an issue](https://github.com/Writality/music-library/issues/new) with a link to the track or album, the artist's name, and which collection you think it fits. Tell me what you like about it too, if you want.

If you know where the artist explains how their music can be used, drop that link in as well. Free to listen does not always mean I can host the audio, so I'll check the terms before adding anything. If it's your own music, let me know how you'd like to be credited and whether I can host it.

Some sources need a login or checkout. That's fine, just send the link. A couple of those are already listed in [ATTRIBUTION.md](ATTRIBUTION.md).

## Send a pull request

You can also add music directly. Include the MP3 in `tracks/<collection>/` and add a track entry to `manifest.json` with a unique integer `id`, `file`, `title`, `artist`, `sourceUrl`, `license`, `licenseUrl`, `attribution`, and `changes`. Add the ID to the appropriate collection's `tracks` list. Use a negative ID to avoid clashing with app tracks. For a new collection, add its `id`, `title`, `description`, and track IDs to `collections` too.

The job on `main` fills in `duration`, `sizeBytes`, and `sha256` after the pull request is merged. Leave those fields out of new entries. You can run `python3 scripts/update_manifest.py` locally if you have `ffprobe` installed.

Not every track has a published license. Use the fields to describe the actual rights, without inventing a Creative Commons license:

- `license`: put the published license or rights status. If the rights holder gave Writality direct permission, use `Used with permission` and explain the permitted use in the pull request.
- `licenseUrl`: link to the published terms, a public permission statement from the rights holder, or the track's section in [ATTRIBUTION.md](ATTRIBUTION.md) documenting permission. Use the full GitHub URL so the app can open it. Do not put `N/A` or a made-up license URL here.
- `sourceUrl`: link to the artist's original page. For an unpublished track, link to the pull request where the artist submitted the original file.
- `attribution`: write the credit the artist requested. `changes`: describe any edits, or use `Original file; no changes.`

I review permission to host and distribute the audio before merging. If permission is unclear, or you cannot provide the audio, open an issue or send a pull request with the source and rights information in [ATTRIBUTION.md](ATTRIBUTION.md); I can add the file after the rights are settled.

Found a wrong title, credit, or broken link? Open an issue or send a pull request.
