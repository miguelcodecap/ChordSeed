POSTS_EN = {}

POSTS_EN['borrowed'] = dict(
slug='borrowed-chords-beatles', img='cover-borrowed-chords-beatles', og='borrowed-chords',
eyebrow='Color', minutes=6,
title='Borrowed chords: the Beatles’ favorite trick',
desc='What borrowed chords are, which ones work in any major key, and how the Beatles used the minor iv, ♭VII and ♭III in songs like In My Life, Hey Jude and Here Comes the Sun.',
card='One chord from outside the key, used at the right moment.',
lede='Some songs have one chord that makes you stop and feel something. Very often it’s a chord “borrowed” from outside the key, and the Beatles were masters at placing it exactly where it hurts (in a good way).',
alt='Lumen reaching through a glowing portal in a tree to borrow a musical note from another world',
body='''
<h2>What is a borrowed chord?</h2>
<p>Every major key has a twin: the minor key that starts on the same note. C major and C minor share the same home, but C minor has darker notes (E♭, A♭ and B♭). A <strong>borrowed chord</strong> is a chord you take from that dark twin and drop into your happy major song.</p>
<p>The result is a moment of shadow, nostalgia or power without leaving home. Musicians also call it <em>modal mixture</em>, but you don’t need the name to use it.</p>

<h2>The four borrowed chords worth knowing</h2>
<table>
<tr><th>Chord</th><th>In C</th><th>In G</th><th>How it feels</th></tr>
<tr><td>minor iv</td><td><code>Fm</code></td><td><code>Cm</code></td><td>Bittersweet, nostalgic. A lump in the throat.</td></tr>
<tr><td>♭VII</td><td><code>B♭</code></td><td><code>F</code></td><td>Big, open, a bit rebellious. Pure rock.</td></tr>
<tr><td>♭VI</td><td><code>A♭</code></td><td><code>E♭</code></td><td>Epic and cinematic, like the sun breaking through.</td></tr>
<tr><td>♭III</td><td><code>E♭</code></td><td><code>B♭</code></td><td>Bold and bright, a sudden change of light.</td></tr>
</table>

<h2>How the Beatles used them</h2>
<h3>The minor iv in “In My Life”</h3>
<p>In the verses (key of A), the harmony goes to D, the normal IV chord, and then turns it into <strong>D minor</strong> before landing back on A. That one note changing, from F♯ to F, is what gives the song its gentle sadness about the past.</p>
<div class="prog"><span>A</span><span>D</span><span>Dm</span><span>A</span><em>IV → iv → I</em></div>

<h3>The ♭VII in the coda of “Hey Jude”</h3>
<p>The long sing-along ending (key of F) repeats a loop with E♭, a chord that isn’t in F major. It makes the ending feel huge and communal, like a stadium singing together.</p>
<div class="prog"><span>F</span><span>E♭</span><span>B♭</span><span>F</span><em>I → ♭VII → IV → I</em></div>

<h3>The ♭III and ♭VII in “Here Comes the Sun”</h3>
<p>In the bridge (key of A), George Harrison cycles through C and G, two chords borrowed from A minor, before arriving at D and A. It feels like clouds moving across the sky before the light returns.</p>
<div class="prog"><span>C</span><span>G</span><span>D</span><span>A</span><em>♭III → ♭VII → IV → I</em></div>

<h2>How to use them in your own songs</h2>
<ul>
<li><strong>Minor iv right before home.</strong> Play IV, then the same chord in minor, then I. It works in almost any ballad: <code>C – F – Fm – C</code>.</li>
<li><strong>♭VII – IV – I for a big ending.</strong> Perfect for the last chorus or a sing-along outro: <code>G – F – C – G</code> in the key of G.</li>
<li><strong>♭VI – ♭VII – I for an epic arrival.</strong> The “hero wins” move: <code>A♭ – B♭ – C</code>.</li>
<li><strong>One at a time.</strong> A borrowed chord is a spice. Use it once in a section, then go back to the normal family so the surprise keeps its power.</li>
</ul>
<p>The best test is your ear: play your progression with and without the borrowed chord and keep the version that gives you goosebumps.</p>
''',
try_text='Turn on <strong>Surprise</strong> in the chord generator and Chordseed suggests borrowed chords that fit your progression, tells you which key they come from and plays them so you can hear the change. Free, in your browser.')

POSTS_EN['reharm'] = dict(
slug='how-to-reharmonize-a-song', img='cover-how-to-reharmonize-a-song', og='reharmonize',
eyebrow='Reharmonization', minutes=7,
title='How to reharmonize a song in 5 simple steps',
desc='A beginner-friendly guide to reharmonization: add sevenths, swap chords that share notes, use secondary dominants, borrowed chords and the tritone substitution, with a before-and-after example.',
card='Same melody, new colors: five moves from easy to jazzy.',
lede='Reharmonizing means keeping the melody and changing the chords underneath it. It’s how a simple song becomes jazzy, moody or cinematic. You can do it with five moves, from very easy to a little daring.',
alt='Lumen the alchemist pouring a glowing potion while musical notes swirl out of the flask',
body='''
<h2>The one rule: respect the melody</h2>
<p>Before changing a chord, look at the melody note that sounds over it. The new chord should either <strong>contain that note</strong> or turn it into a pretty color (a 7th, 9th or 6th). If the melody note clashes, try another option. Your ear will tell you right away.</p>
<p>We’ll reharmonize this simple progression in C:</p>
<div class="prog"><span>C</span><span>F</span><span>G</span><span>C</span><em>the original</em></div>

<h2>Step 1: add sevenths</h2>
<p>The easiest upgrade. Add one note to each chord and everything sounds warmer and more “grown up”.</p>
<div class="prog"><span>Cmaj7</span><span>Fmaj7</span><span>G7</span><span>Cmaj7</span><em>instantly smoother</em></div>

<h2>Step 2: swap chords that share notes</h2>
<p>Chords that share two notes can replace each other. C (C E G) and Am (A C E) share C and E. F (F A C) and Dm (D F A) share F and A. The melody usually still fits, but the mood shifts.</p>
<table>
<tr><th>Original</th><th>Try instead</th><th>Effect</th></tr>
<tr><td><code>C</code></td><td><code>Am</code> or <code>Em</code></td><td>Softer, more emotional</td></tr>
<tr><td><code>F</code></td><td><code>Dm</code></td><td>Smoother motion towards G</td></tr>
<tr><td><code>G</code></td><td><code>Em</code></td><td>Less push, more floating</td></tr>
</table>

<h2>Step 3: add a secondary dominant</h2>
<p>Any chord can have its own “tension chord” that leads into it. To make Dm feel inevitable, play <strong>A7</strong> right before it. To lead into Am, use <strong>E7</strong>. These chords add a strong sense of motion.</p>
<div class="prog"><span>C</span><span>A7</span><span>Dm7</span><span>G7</span><span>C</span><em>A7 pulls into Dm</em></div>

<h2>Step 4: borrow a chord</h2>
<p>Turn the IV chord into a minor chord for a bittersweet moment. In C, F becomes <strong>Fm</strong>. It works especially well right before going back home. (We explain this one in detail in <a href="../borrowed-chords-beatles/">Borrowed chords: the Beatles’ favorite trick</a>.)</p>
<div class="prog"><span>C</span><span>F</span><span>Fm</span><span>C</span><em>nostalgic</em></div>

<h2>Step 5: the tritone substitution</h2>
<p>This is the jazz move. Replace G7 with <strong>D♭7</strong>. Both chords share the two notes that create the tension (B and F, also spelled C♭ and F), so D♭7 still wants to go to C, but the bass slides down by a half step. It sounds smooth and sophisticated.</p>
<div class="prog"><span>Dm7</span><span>D♭7</span><span>Cmaj7</span><em>the bass slides D → D♭ → C</em></div>

<h2>Before and after</h2>
<p>Put a few of these moves together and the same four bars sound like a different song:</p>
<div class="prog"><span>C</span><span>F</span><span>G</span><span>C</span><em>before</em></div>
<div class="prog"><span>Cmaj7</span><span>A7</span><span>Dm7</span><span>Fm</span><span>D♭7</span><span>Cmaj7</span><em>after</em></div>
<p>You don’t have to use every trick at once. Often one well-placed change is enough. Try a move, sing the melody over it, and keep it only if it serves the song.</p>
''',
try_text='Open <strong>Enrich my chords</strong> in Chordseed, paste your progression and pick a style. It suggests sevenths, substitutions and passing chords, explains each one and plays the result on a real instrument. Free, in your browser.')

POSTS_EN['key'] = dict(
slug='how-to-change-key-in-a-song', img='cover-how-to-change-key-in-a-song', og='change-key',
eyebrow='Key changes', minutes=6,
title='How to change key in a song (and lift the last chorus)',
desc='Three easy ways to modulate: the sudden lift, the dominant chord trick and the pivot chord. Includes a chart of the chord to play before each new key.',
card='The sudden lift, the dominant trick and the pivot chord.',
lede='A key change can make the last chorus feel like it’s taking off. Done badly, it sounds like a mistake. Here are three ways to do it, from the most dramatic to the smoothest.',
alt='Lumen crossing a glowing bridge over a river from one part of the forest to another',
body='''
<h2>Why change key at all?</h2>
<p>When a song repeats the chorus several times, the energy can drop. Moving everything up gives the listener a fresh lift without writing anything new. Some songs change key between verse and chorus to create contrast, and some (like Beyoncé’s “Love on Top”) do it several times in a row for fun.</p>

<h2>1. The sudden lift</h2>
<p>Just stop and start the next chorus one or two steps higher. No preparation. It’s bold and very common in pop ballads; Whitney Houston’s “I Will Always Love You” is the classic example, right after the dramatic pause.</p>
<div class="prog"><span>C</span><span>G</span><span>Am</span><span>F</span><em style="margin:0 4px 0 0">→</em><span>D</span><span>A</span><span>Bm</span><span>G</span><em>chorus in C, then in D</em></div>
<p>A whole step (two frets) up is the safest jump. A half step (one fret) is more subtle. More than that and singers start to suffer.</p>

<h2>2. The dominant trick</h2>
<p>To make the jump feel prepared, play the <strong>V7 chord of the new key</strong> right before it. That chord creates tension that only the new key can resolve.</p>
<div class="prog"><span>C</span><span>G</span><span>F</span><span>A7</span><em style="margin:0 4px 0 0">→</em><span>D</span><em>A7 points straight to D</em></div>
<table>
<tr><th>From C to…</th><th>Play this before</th><th>Distance</th></tr>
<tr><td><code>D♭</code></td><td><code>A♭7</code></td><td>half step up</td></tr>
<tr><td><code>D</code></td><td><code>A7</code></td><td>whole step up</td></tr>
<tr><td><code>E♭</code></td><td><code>B♭7</code></td><td>minor third up</td></tr>
<tr><td><code>F</code></td><td><code>C7</code></td><td>a fourth up</td></tr>
<tr><td><code>G</code></td><td><code>D7</code></td><td>a fifth up</td></tr>
<tr><td><code>A</code></td><td><code>E7</code></td><td>to a brighter key</td></tr>
</table>
<p>The rule is simple: the chord before the new key is the chord built on the note <strong>five steps above</strong> the new key, with a 7.</p>

<h2>3. The pivot chord</h2>
<p>The smoothest method. Find a chord that belongs to <strong>both</strong> keys and use it as a bridge. C major and G major share C, Em, G and Am. If you play Am, the ear hears it as part of C… and then you treat it as part of G:</p>
<div class="prog"><span>C</span><span>F</span><span>Am</span><span>D7</span><span>G</span><em>Am is the bridge, D7 confirms G</em></div>
<p>This kind of change is so smooth that many listeners won’t notice it. They’ll just feel that the song opened up.</p>

<h2>Bonus: go to the relative minor</h2>
<p>C major and A minor use exactly the same notes. Moving your verse to Am (with an E7 before it) gives you a darker section without any new notes to learn.</p>
<div class="prog"><span>C</span><span>F</span><span>E7</span><span>Am</span><em>a darker turn</em></div>

<h2>Quick checklist</h2>
<ul>
<li>Choose the new key based on the singer’s range, not just on the guitar.</li>
<li>Prepare it with the V7 of the new key unless you want a sudden jolt.</li>
<li>Change key at the start of a section, not in the middle of a phrase.</li>
<li>Once you arrive, stay there long enough for the ear to accept it as home.</li>
</ul>
''',
try_text='Use <strong>Change key</strong> in Chordseed: choose where you are and where you want to go, and it shows you paths to get there, with the bridge and pivot chords marked, plays each one and draws the trip on the circle of fifths. Free, in your browser.')

POSTS_EN['numbers'] = dict(
slug='chord-numbers-roman-numerals', img='cover-chord-numbers-roman-numerals', og='roman-numerals',
eyebrow='Theory basics', minutes=7,
title='Chord numbers explained: play any song in any key',
desc='What I, IV, V and vi mean, the chord families of the most common guitar keys, the Nashville number system, how to transpose a progression and how to find the key of a song.',
card='I, IV, V, vi: the code musicians use to talk about chords.',
lede='When musicians say “it’s a one-four-five” they’re using a secret code that works in every key. Learn it once and you’ll be able to transpose songs, find their key and talk with any band.',
alt='Lumen pointing his lantern at seven glowing circles carved into an ancient tree, one for each chord of the key',
body='''
<h2>Every key has a family of seven chords</h2>
<p>Take a major scale, build a chord on each note using only notes from that scale, and you get seven chords. They always follow the same pattern of major and minor:</p>
<table>
<tr><th>Number</th><th>I</th><th>ii</th><th>iii</th><th>IV</th><th>V</th><th>vi</th><th>vii°</th></tr>
<tr><td>Type</td><td>major</td><td>minor</td><td>minor</td><td>major</td><td>major</td><td>minor</td><td>dim</td></tr>
</table>
<p>Capital Roman numerals mean major chords, lowercase means minor, and the little circle means diminished. The pattern never changes, only the letter names do.</p>

<h2>The chord families of the most common keys</h2>
<table>
<tr><th>Key</th><th>I</th><th>ii</th><th>iii</th><th>IV</th><th>V</th><th>vi</th></tr>
<tr><td><strong>C</strong></td><td><code>C</code></td><td><code>Dm</code></td><td><code>Em</code></td><td><code>F</code></td><td><code>G</code></td><td><code>Am</code></td></tr>
<tr><td><strong>G</strong></td><td><code>G</code></td><td><code>Am</code></td><td><code>Bm</code></td><td><code>C</code></td><td><code>D</code></td><td><code>Em</code></td></tr>
<tr><td><strong>D</strong></td><td><code>D</code></td><td><code>Em</code></td><td><code>F♯m</code></td><td><code>G</code></td><td><code>A</code></td><td><code>Bm</code></td></tr>
<tr><td><strong>A</strong></td><td><code>A</code></td><td><code>Bm</code></td><td><code>C♯m</code></td><td><code>D</code></td><td><code>E</code></td><td><code>F♯m</code></td></tr>
<tr><td><strong>E</strong></td><td><code>E</code></td><td><code>F♯m</code></td><td><code>G♯m</code></td><td><code>A</code></td><td><code>B</code></td><td><code>C♯m</code></td></tr>
<tr><td><strong>F</strong></td><td><code>F</code></td><td><code>Gm</code></td><td><code>Am</code></td><td><code>B♭</code></td><td><code>C</code></td><td><code>Dm</code></td></tr>
</table>
<p>The vii° chord is left out because it’s rarely used in pop and rock.</p>

<h2>What each number does</h2>
<ul>
<li><strong>I</strong> is home. Songs usually start and end here.</li>
<li><strong>IV</strong> is a step away from home: open and relaxed.</li>
<li><strong>V</strong> is tension. It wants to go back to I.</li>
<li><strong>vi</strong> is the emotional, minor side of home.</li>
<li><strong>ii</strong> and <strong>iii</strong> are softer connectors, often leading to V or IV.</li>
</ul>

<h2>Transposing becomes easy</h2>
<p>The famous I–V–vi–IV progression is the same idea in every key. Only the letters change:</p>
<div class="prog"><span>C</span><span>G</span><span>Am</span><span>F</span><em>in C</em></div>
<div class="prog"><span>G</span><span>D</span><span>Em</span><span>C</span><em>in G</em></div>
<div class="prog"><span>D</span><span>A</span><span>Bm</span><span>G</span><em>in D</em></div>
<p>So if a song is too low for your voice, write it down in numbers, choose a higher key and read the new letters from the table. A capo does the same on guitar: with a capo on the 2nd fret, G shapes sound in the key of A.</p>

<h2>The Nashville number system</h2>
<p>Session players in Nashville use the same idea with regular numbers: <strong>1 – 5 – 6m – 4</strong>. The band can follow a chart in any key the singer asks for, on the spot. Roman numerals or Nashville numbers, it’s the same code.</p>

<h2>How to find the key of a song</h2>
<ol>
<li><strong>Listen for home.</strong> The chord that feels like rest, usually the first or last one, is probably I.</li>
<li><strong>Check the family.</strong> Look for the row in the table that contains all (or almost all) the chords of the song.</li>
<li><strong>Follow the 7 chord.</strong> A chord like D7 almost always points to its I chord, G.</li>
<li><strong>Major or minor?</strong> If home is a minor chord (say Am), the song is in A minor, which shares its family with C major.</li>
</ol>
''',
try_text='Paste any progression into <strong>Analyze my progression</strong> in Chordseed. It finds the key, labels every chord with its number and draws the tension curve so you can see what each chord does. Free, in your browser.')

POSTS_EN['lofi'] = dict(
slug='lofi-chord-progressions', img='cover-lofi-chord-progressions', og='lofi',
eyebrow='Moods', minutes=6,
title='6 lo-fi chord progressions (and why they sound so chill)',
desc='Lo-fi hip hop chord progressions you can play today: seventh and ninth chords, ii–V–I loops and minor vamps, with tips on tempo, voicings and swing.',
card='Sevenths, ninths and slow loops for that late-night feeling.',
lede='Lo-fi music sounds relaxed and a little nostalgic, like studying late at night with rain on the window. Most of that feeling comes from the chords. Here are six progressions to start with and the reasons they work.',
alt='Lumen with headphones playing a small keyboard in a cozy tree house at night, a cup of tea on the desk',
body='''
<h2>What makes chords sound “lo-fi”?</h2>
<ul>
<li><strong>Sevenths and ninths.</strong> Instead of plain C or Am, lo-fi uses Cmaj7, Am9, Dm7. The extra notes make chords soft and unresolved.</li>
<li><strong>Short loops.</strong> Two or four chords repeating over and over, so the listener can relax into them.</li>
<li><strong>Jazz movement.</strong> Many loops borrow the ii–V–I from jazz, but slowed down.</li>
<li><strong>Slow tempo with swing.</strong> Usually 70–90 BPM, with drums that feel a little lazy and behind the beat.</li>
</ul>

<h2>1. The descending loop</h2>
<p>Each chord steps down by one note. It feels like a slow sigh.</p>
<div class="prog"><span>Fmaj7</span><span>Em7</span><span>Dm7</span><span>Cmaj7</span><em>IV – iii – ii – I in C</em></div>

<h2>2. The jazz cycle</h2>
<p>The classic 1–6–2–5. It never feels finished, which is perfect for a loop.</p>
<div class="prog"><span>Cmaj7</span><span>Am7</span><span>Dm7</span><span>G7</span><em>I – vi – ii – V</em></div>

<h2>3. The ii–V–I with ninths</h2>
<p>The same jazz move with richer colors. Swap G9 for G13 if you want it even dreamier.</p>
<div class="prog"><span>Dm9</span><span>G9</span><span>Cmaj9</span><span>Cmaj9</span><em>ii – V – I</em></div>

<h2>4. The two-chord minor vamp</h2>
<p>Only two chords, but with ninths they sound deep. Great for melodies and samples on top.</p>
<div class="prog"><span>Am9</span><span>Dm9</span><em>i – iv in A minor</em></div>

<h2>5. The bittersweet minor</h2>
<p>The E7 adds a moment of tension before falling back to Am. Moody and cinematic.</p>
<div class="prog"><span>Fmaj7</span><span>E7</span><span>Am7</span><span>Am7</span><em>VI – V – i in A minor</em></div>

<h2>6. The neo-soul lift</h2>
<p>The A7 isn’t in the key of C; it’s a secondary dominant that pulls into Dm7 and gives the loop a soulful lift.</p>
<div class="prog"><span>Cmaj7</span><span>A7</span><span>Dm7</span><span>G7</span><em>I – VI7 – ii – V</em></div>

<h2>Tips to make it sound right</h2>
<ul>
<li><strong>Play soft.</strong> Electric piano or a clean, mellow guitar works best. Avoid strong strumming.</li>
<li><strong>Keep voicings close.</strong> Move as few fingers as possible between chords so the loop flows.</li>
<li><strong>Let it breathe.</strong> One chord per bar, sometimes two bars, is plenty.</li>
<li><strong>Add texture.</strong> Vinyl crackle, rain or tape hiss are part of the genre, but the chords come first.</li>
</ul>
''',
try_text='In Chordseed, choose the <strong>Lo-fi hip hop</strong> style and a dreamy or melancholic mood. The generator suggests relaxed sevenths and ninths and plays your loop with a lazy beat and bass behind it. Free, in your browser.')
