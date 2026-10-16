# Narration and voice

## Contents
1. Writing beats
2. Takes
3. Generating with the ElevenLabs connector
4. Getting the audio into the workspace
5. How splitting works, and when it fails
6. Alternatives

## 1. Writing beats

A beat is one visual change plus the words that describe it. The scene wraps that change in `with self.beat("id")` and the change lasts as long as the clip.

- **Split where the picture changes.** "The first batch fails. The second succeeds. Then the first is retried" can be one beat with three timed motions inside, or three beats. Prefer one beat with `self.wait()` between motions when the sentences flow together, and separate beats when the picture changes completely.
- **Write for the ear.** "partition one" not "p1"; "acks all" not "acks=all"; "the send call" not "send()". Spell versions the way they're said ("Kafka three", "one-oh-one"). The on-screen caption can show the code form.
- **Short, declarative sentences.** TTS handles them well and they leave room for the animation.
- **Numbers.** With `eleven_v4`/`eleven_v3`, write numbers as you want them read; for other models spell them out.
- **Avoid sentences that depend on a visual the viewer hasn't seen yet.** The voice and picture start together; a beat should never refer to something that appears only at its end.

## 2. Takes

Generate one audio file per TAKE (a group of consecutive scenes), not per beat: per-beat generation means dozens of downloads, and per-scene still means many. Keep each take under ~2,000 characters. Long takes risk model limits and make boundaries harder to find.

Beats in a take are joined with `[long pause]` (`narration.PAUSE`). That tag works on `eleven_v4` and `eleven_v3`. For models without tags (`eleven_multilingual_v2`, `flash`, `turbo`) use `<break time="1.5s" />`, but those models handle only a few breaks per request, so prefer v4.

Cost is about 1 credit per character. An 8 to 9 minute episode is ~8,500 characters. Rewording one sentence means regenerating its whole take, so get the facts right before generating.

## 3. Generating with the ElevenLabs connector

1. **Find the voice.** Call `creative_list_voices` with no filters and look for `category: "cloned"` (e.g. "My Voice 2026-10-15"). Searching by the user's name returns public library voices with similar names. Those are not the user's voice.
2. **Read the model guide once** (`creative_get_model_guide`, `eleven_v4`) if pause or tag behavior matters.
3. **Create one flow** (`creative_create_flow`) named after the episode, so all takes live together and the user can find them.
4. **Generate each take** with `creative_generate_speech`: `model_id: eleven_v4`, the cloned `voice_id`, `prompt: narration.take_text(<take>)`, and **`generations_count: 1`**. The connector defaults to 4 variations, which quadruples the cost; you can't listen to pick between them, and the user can regenerate a take in the flow if one sounds off. Tell the user why you chose 1. Fire all takes in one turn; they generate in parallel.
5. **Poll** `creative_get_flow_run_status` with all session ids until `all_completed`. Each result has `duration_secs` and a signed `content_url` that expires after ~2 hours.

Never re-call a generation to "retry": each call is a new paid generation.

## 4. Getting the audio into the workspace

Try a direct download once:

```bash
curl -sS -o take.mp3 -w "%{http_code}\n" "<content_url>"
```

If the sandbox blocks the host (`CONNECT tunnel failed, response 403`), don't try other routes. Send the user, in one message:
- a numbered list of take links, each labelled with its scenes and duration,
- the time the links expire,
- the flow link as a fallback,
- a request to attach the mp3s here, in any order.

Attached files arrive with generic names (`New_tts_node-1.mp3` ...). Match them to takes by duration (`ffprobe -show_entries format=duration`) and copy them to `audio/takes/<take>.mp3`.

## 5. How splitting works, and when it fails

`tools/split_narration.py` finds every silence (ffmpeg `silencedetect`, −38 dB, ≥ 0.3 s), then picks one boundary per beat break by dynamic programming. Each candidate is scored on two things: how long the pause is, and how close it sits to where that boundary should be given the characters spoken before it.

Picking the N−1 longest pauses alone fails: a long dramatic pause inside a sentence can be as long as a real beat break (it happened: 1.05 s vs 1.05 s). The expected-position term fixes that.

Checks after splitting:
- Every beat prints its speaking rate. Normal is ~12 to 19 chars/s. Outliers are flagged.
- "shortest boundary" vs "longest unused pause" in the header shows the margin. A margin under ~0.3 s is worth an ear check by the user.
- If too few pauses are found, the take was generated without pauses: check `PAUSE` and the model.

## 6. Alternatives

- **The user records their own voice:** have them read the take text with a clear 1 to 2 s pause between beats, then split the same way.
- **Silent draft:** scenes render with estimated timing (2.6 words/s) when no manifest exists, which is good enough for visual review.
