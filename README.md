# BSL Translator

**Track:** Languages
**Team:** WIMD
**▶ Try it:** [TO FILL: https://YOUR-USERNAME.github.io/bsl-translator/] (Chrome, webcam, no install, no video leaves your device)

## The problem
About 151,000 people in the UK use British Sign Language (87,000 of them Deaf), but there are only about 900 registered interpreters, so everyday conversations often have no one to translate. Most sign-language tech is built for American Sign Language, which is a different language with a one-handed alphabet. BSL's is two-handed.

## What we built
A website that turns BSL signed to a webcam into English sentences, shown as live captions and spoken aloud. It recognises **words** our team recorded and the **fingerspelled alphabet**, rearranges BSL word order into English (*YOU NAME WHAT* → "What is your name?"), and lets anyone **teach it their own hands** in seconds. Crossing your arms in an ✕ deletes the last sign.

## How it works
**Data:** 19,713 two-handed alphabet examples (22 letters + 10) from a public Kaggle dataset, plus 399 recordings of 19 words (21 per word) made entirely by our team, with consent (no outside dataset). Each example is MediaPipe's 21 points per hand, centred, scaled and mirrored, so position, distance and handedness don't matter.
**Models:** a small neural network for letters (beat logistic regression and a random forest on speed, with equal accuracy), and nearest-neighbour matching for words, which works from very few examples and learns new words instantly. Built-in grammar rules turn signs into English, with optional AI (Gemini) rewriting.

## Results
| Test | Accuracy |
|---|---|
| Baseline (always guess the most common letter) | 5.0% |
| Our letter model, held-out data from the **same dataset** | 99.9% |
| Our letter model, **our own hands** (1,787 frames of the 11 letters we taught, mostly ones it was getting wrong) | **7.6%** |
| …after "teaching" it our hands (15 letters incl. C, H, J, Y; each recording tested using only our *other* recordings) | **90.5%** |
| …stricter: a whole recording session left out (4 letters taught in 2+ sessions) | 53.1% |
| Words: 15 of our 19 words × 5 attempts, signed by a teammate who did **not** record any training samples (baseline 1/19 = 5.3%) | **96%** (72/75; *world* once not detected at all, *am* and *we* each missed once) |

99.9% was too good to be true: the dataset comes from very few signers. On our hands the model collapsed, reading most letters as "V". We checked it wasn't a bug (camera shape, mirroring and depth fixes didn't help); our hands simply looked different from the dataset's. Teaching fixed most letters, but O (35%) stayed weak and H (one recording) failed, and our teaching tests used the same people who taught, so they're optimistic. We only track hands, so questions shown by raised eyebrows are missed. It worked equally well for each teammate, but only when signs were clear and not too fast. We could only test on our own small team, not a wide range of signers.

**What we learned**
- **BSL has different signs for the same word**, depending on region and signer, so a translator trained on one person's signs can miss another's.
- **BSL grammar is different from English grammar** (e.g. question words come at the end), so translation isn't word-for-word and needed its own step.
- **There's very little accessible help for BSL signers.** Most websites and online services offer only written English, a phone line or a chatbot, with no live sign-language translation, even though English may be a Deaf person's second language.
- **There are very few BSL datasets.** Most sign-language data is American Sign Language. The BSL word datasets we found were raw video or restricted to academic researchers, so we recorded our own words.

## What we'd do next
1. Train on many more signers with Deaf BSL users involved (e.g. BBC–Oxford's BOBSL dataset, with academic access).
2. Add face and motion tracking for questions and moving signs.

*Prototype only, not a replacement for an interpreter. Only hand-point coordinates are stored, never video.*

## Sources
Data: [BSL Numbers & Alphabet Hand Position for MediaPipe (Kaggle)](https://www.kaggle.com/datasets/erentatepe/bsl-numbers-and-alphabet-hand-position-for-mediapipe) · Models: [MediaPipe Hand](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) and [Pose Landmarker](https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker), [Gemini API](https://ai.google.dev/gemini-api/docs) (optional) · Libraries: [scikit-learn](https://scikit-learn.org), pandas, NumPy · Facts: [British Deaf Association](https://bda.org.uk/bsl-deaf-culture/) · Future work: [BOBSL](https://www.robots.ox.ac.uk/~vgg/data/bobsl/), [BSLDict](https://www.robots.ox.ac.uk/~vgg/research/bsldict/)
AI tools: [Claude](https://claude.ai) (Anthropic): planning, writing the website and training code, and drafting this write-up
Code: `index.html` (website) · `train_fingerspelling.ipynb` (training and evaluation)
