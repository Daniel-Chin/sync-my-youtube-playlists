yt-dlp 'https://www.youtube.com/playlist?list=LL' \
    --skip-download \
    --dump-json \
    --write-info-json \
    --output './Liked/%(id)s.%(ext)s' \
    # --cookies ~/temp/cookies.txt \
    --cookies ~/temp/cookies.firefox-private.txt \
    # --cookies-from-browser firefox \
    2> ./err.txt \
    | jq -r '{
        id: .id,
        title: .title,
        channel: .channel,
        uploader: .uploader,
        description: .description,
        categories: .categories,
        chapters: .chapters,
        duration: .duration,
        _filename: ._filename,
        filename: .filename,
        _type: ._type,
        _version: ._version,
        acodec: .acodec,
        abr: .abr,
        asr: .asr,
        audio_channels: .audio_channels
    }' \
    > ./meta.json
