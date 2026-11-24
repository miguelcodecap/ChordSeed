POSTS_ES = {}

POSTS_ES['borrowed'] = dict(
slug='acordes-prestados-beatles', eyebrow='Color', minutes=6,
title='Acordes prestados: el truco favorito de los Beatles',
desc='Qué son los acordes prestados, cuáles funcionan en cualquier tonalidad mayor y cómo los Beatles usaron el iv menor, el ♭VII y el ♭III en In My Life, Hey Jude y Here Comes the Sun.',
card='Un acorde de fuera de la tonalidad, en el momento justo.',
lede='Hay canciones con un acorde que te detiene y te hace sentir algo. Muchas veces es un acorde “prestado” de fuera de la tonalidad, y los Beatles eran maestros en ponerlo justo donde duele (en el buen sentido).',
alt='Lumen atravesando un portal luminoso en un árbol para tomar prestada una nota musical de otro mundo',
body='''
<h2>¿Qué es un acorde prestado?</h2>
<p>Cada tonalidad mayor tiene una gemela: la tonalidad menor que empieza en la misma nota. Do mayor (C) y Do menor (Cm) comparten la misma casa, pero la menor tiene notas más oscuras (E♭, A♭ y B♭). Un <strong>acorde prestado</strong> es un acorde que tomas de esa gemela oscura y lo pones en tu canción mayor y alegre.</p>
<p>El resultado es un momento de sombra, nostalgia o fuerza sin salir de casa. También se le llama <em>intercambio modal</em>, pero no necesitas saber el nombre para usarlo.</p>

<h2>Los cuatro acordes prestados que vale la pena conocer</h2>
<table>
<tr><th>Acorde</th><th>En C</th><th>En G</th><th>Cómo se siente</th></tr>
<tr><td>iv menor</td><td><code>Fm</code></td><td><code>Cm</code></td><td>Agridulce, nostálgico. Un nudo en la garganta.</td></tr>
<tr><td>♭VII</td><td><code>B♭</code></td><td><code>F</code></td><td>Grande, abierto, un poco rebelde. Rock puro.</td></tr>
<tr><td>♭VI</td><td><code>A♭</code></td><td><code>E♭</code></td><td>Épico y de película, como el sol saliendo entre nubes.</td></tr>
<tr><td>♭III</td><td><code>E♭</code></td><td><code>B♭</code></td><td>Audaz y luminoso, un cambio repentino de luz.</td></tr>
</table>

<h2>Cómo los usaron los Beatles</h2>
<h3>El iv menor en “In My Life”</h3>
<p>En las estrofas (tonalidad de A), la armonía va a D, el acorde IV normal, y luego lo convierte en <strong>Re menor (Dm)</strong> antes de volver a A. Ese cambio de una sola nota, de F♯ a F, es lo que le da a la canción su tristeza suave por el pasado.</p>
<div class="prog"><span>A</span><span>D</span><span>Dm</span><span>A</span><em>IV → iv → I</em></div>

<h3>El ♭VII en el final de “Hey Jude”</h3>
<p>El largo final para cantar en coro (tonalidad de F) repite un ciclo con E♭, un acorde que no está en Fa mayor. Hace que el final se sienta enorme y colectivo, como un estadio cantando junto.</p>
<div class="prog"><span>F</span><span>E♭</span><span>B♭</span><span>F</span><em>I → ♭VII → IV → I</em></div>

<h3>El ♭III y el ♭VII en “Here Comes the Sun”</h3>
<p>En el puente (tonalidad de A), George Harrison pasa por C y G, dos acordes prestados de La menor, antes de llegar a D y A. Se siente como nubes que pasan antes de que vuelva la luz.</p>
<div class="prog"><span>C</span><span>G</span><span>D</span><span>A</span><em>♭III → ♭VII → IV → I</em></div>

<h2>Cómo usarlos en tus canciones</h2>
<ul>
<li><strong>iv menor justo antes de volver a casa.</strong> Toca el IV, luego el mismo acorde en menor y después el I. Funciona en casi cualquier balada: <code>C – F – Fm – C</code>.</li>
<li><strong>♭VII – IV – I para un gran final.</strong> Perfecto para el último coro o un cierre para cantar todos: <code>G – F – C – G</code> en tonalidad de G.</li>
<li><strong>♭VI – ♭VII – I para una llegada épica.</strong> El movimiento de “el héroe gana”: <code>A♭ – B♭ – C</code>.</li>
<li><strong>De uno en uno.</strong> Un acorde prestado es una especia. Úsalo una vez por sección y vuelve a la familia normal para que la sorpresa no pierda fuerza.</li>
</ul>
<p>La mejor prueba es tu oído: toca tu progresión con y sin el acorde prestado, y quédate con la versión que te pone la piel de gallina.</p>
''',
try_text='Activa <strong>Sorpresa</strong> en el generador de acordes y Chordseed te sugiere acordes prestados que encajan con tu progresión, te dice de qué tonalidad vienen y los toca para que escuches el cambio. Gratis, en tu navegador.')

POSTS_ES['reharm'] = dict(
slug='como-rearmonizar-una-cancion', eyebrow='Rearmonización', minutes=7,
title='Cómo rearmonizar una canción en 5 pasos simples',
desc='Guía para principiantes sobre rearmonización: agrega séptimas, cambia acordes que comparten notas, usa dominantes secundarias, acordes prestados y la sustitución tritonal, con un ejemplo de antes y después.',
card='La misma melodía, colores nuevos: cinco movimientos de fácil a jazzero.',
lede='Rearmonizar es mantener la melodía y cambiar los acordes que van debajo. Así una canción sencilla se vuelve jazzera, melancólica o de película. Puedes hacerlo con cinco movimientos, de muy fácil a un poco atrevido.',
alt='Lumen, el alquimista, sirviendo una poción luminosa mientras salen notas musicales del frasco',
body='''
<h2>La única regla: respeta la melodía</h2>
<p>Antes de cambiar un acorde, mira qué nota de la melodía suena encima. El acorde nuevo debe <strong>contener esa nota</strong> o convertirla en un color bonito (una 7ª, 9ª o 6ª). Si la nota choca, prueba otra opción. Tu oído te lo dirá al instante.</p>
<p>Vamos a rearmonizar esta progresión sencilla en C:</p>
<div class="prog"><span>C</span><span>F</span><span>G</span><span>C</span><em>la original</em></div>

<h2>Paso 1: agrega séptimas</h2>
<p>La mejora más fácil. Agrega una nota a cada acorde y todo suena más cálido y más “maduro”.</p>
<div class="prog"><span>Cmaj7</span><span>Fmaj7</span><span>G7</span><span>Cmaj7</span><em>más suave al instante</em></div>

<h2>Paso 2: cambia acordes que comparten notas</h2>
<p>Los acordes que comparten dos notas pueden reemplazarse entre sí. C (C E G) y Am (A C E) comparten C y E. F (F A C) y Dm (D F A) comparten F y A. La melodía casi siempre sigue encajando, pero el ánimo cambia.</p>
<table>
<tr><th>Original</th><th>Prueba con</th><th>Efecto</th></tr>
<tr><td><code>C</code></td><td><code>Am</code> o <code>Em</code></td><td>Más suave, más emotivo</td></tr>
<tr><td><code>F</code></td><td><code>Dm</code></td><td>Un paso más fluido hacia G</td></tr>
<tr><td><code>G</code></td><td><code>Em</code></td><td>Menos empuje, más flotante</td></tr>
</table>

<h2>Paso 3: agrega una dominante secundaria</h2>
<p>Cualquier acorde puede tener su propio “acorde de tensión” que lo anuncia. Para que Dm se sienta inevitable, toca <strong>A7</strong> justo antes. Para llegar a Am, usa <strong>E7</strong>. Estos acordes le dan mucho movimiento a la progresión.</p>
<div class="prog"><span>C</span><span>A7</span><span>Dm7</span><span>G7</span><span>C</span><em>A7 empuja hacia Dm</em></div>

<h2>Paso 4: toma prestado un acorde</h2>
<p>Convierte el acorde IV en menor para un momento agridulce. En C, F se vuelve <strong>Fm</strong>. Funciona especialmente bien justo antes de volver a casa. (Lo explicamos a fondo en <a href="../acordes-prestados-beatles/">Acordes prestados: el truco favorito de los Beatles</a>.)</p>
<div class="prog"><span>C</span><span>F</span><span>Fm</span><span>C</span><em>nostálgico</em></div>

<h2>Paso 5: la sustitución tritonal</h2>
<p>Este es el movimiento del jazz. Cambia G7 por <strong>D♭7</strong>. Los dos acordes comparten las dos notas que crean la tensión (B y F; en D♭7 la B se escribe C♭), así que D♭7 también quiere ir a C, pero el bajo baja medio tono. Suena suave y sofisticado.</p>
<div class="prog"><span>Dm7</span><span>D♭7</span><span>Cmaj7</span><em>el bajo baja D → D♭ → C</em></div>

<h2>Antes y después</h2>
<p>Junta algunos de estos movimientos y los mismos cuatro compases suenan como otra canción:</p>
<div class="prog"><span>C</span><span>F</span><span>G</span><span>C</span><em>antes</em></div>
<div class="prog"><span>Cmaj7</span><span>A7</span><span>Dm7</span><span>Fm</span><span>D♭7</span><span>Cmaj7</span><em>después</em></div>
<p>No tienes que usar todos los trucos a la vez. Muchas veces basta con un cambio bien puesto. Prueba un movimiento, canta la melodía encima y quédate con él solo si le sirve a la canción.</p>
''',
try_text='Abre <strong>Enriquecer mis acordes</strong> en Chordseed, pon tu progresión y elige un estilo. Te sugiere séptimas, sustituciones y acordes de paso, te explica cada uno y toca el resultado con un instrumento real. Gratis, en tu navegador.')

POSTS_ES['key'] = dict(
slug='como-cambiar-de-tonalidad-en-una-cancion', eyebrow='Cambios de tonalidad', minutes=6,
title='Cómo cambiar de tonalidad en una canción (y subir el último coro)',
desc='Tres formas fáciles de modular: el salto repentino, el truco de la dominante y el acorde pivote. Incluye una tabla con el acorde que debes tocar antes de cada tonalidad nueva.',
card='El salto repentino, el truco de la dominante y el acorde pivote.',
lede='Un cambio de tonalidad puede hacer que el último coro despegue. Mal hecho, suena a error. Aquí tienes tres formas de hacerlo, de la más dramática a la más suave.',
alt='Lumen cruzando un puente luminoso sobre un río, de una parte del bosque a otra',
body='''
<h2>¿Para qué cambiar de tonalidad?</h2>
<p>Cuando una canción repite el coro varias veces, la energía puede bajar. Subir todo le da al oyente un impulso nuevo sin escribir nada más. Algunas canciones cambian de tonalidad entre la estrofa y el coro para crear contraste, y otras (como “Love on Top” de Beyoncé) lo hacen varias veces seguidas por pura diversión.</p>

<h2>1. El salto repentino</h2>
<p>Simplemente para y empieza el siguiente coro uno o dos semitonos más arriba. Sin preparación. Es atrevido y muy común en baladas pop; “I Will Always Love You” de Whitney Houston es el ejemplo clásico, justo después de la pausa dramática.</p>
<div class="prog"><span>C</span><span>G</span><span>Am</span><span>F</span><em style="margin:0 4px 0 0">→</em><span>D</span><span>A</span><span>Bm</span><span>G</span><em>coro en C, luego en D</em></div>
<p>Subir un tono (dos trastes) es el salto más seguro. Medio tono (un traste) es más sutil. Más que eso y quien canta empieza a sufrir.</p>

<h2>2. El truco de la dominante</h2>
<p>Para que el salto se sienta preparado, toca el <strong>acorde V7 de la tonalidad nueva</strong> justo antes. Ese acorde crea una tensión que solo la tonalidad nueva puede resolver.</p>
<div class="prog"><span>C</span><span>G</span><span>F</span><span>A7</span><em style="margin:0 4px 0 0">→</em><span>D</span><em>A7 apunta directo a D</em></div>
<table>
<tr><th>De C a…</th><th>Toca antes</th><th>Distancia</th></tr>
<tr><td><code>D♭</code></td><td><code>A♭7</code></td><td>medio tono arriba</td></tr>
<tr><td><code>D</code></td><td><code>A7</code></td><td>un tono arriba</td></tr>
<tr><td><code>E♭</code></td><td><code>B♭7</code></td><td>tercera menor arriba</td></tr>
<tr><td><code>F</code></td><td><code>C7</code></td><td>una cuarta arriba</td></tr>
<tr><td><code>G</code></td><td><code>D7</code></td><td>una quinta arriba</td></tr>
<tr><td><code>A</code></td><td><code>E7</code></td><td>a una tonalidad más brillante</td></tr>
</table>
<p>La regla es simple: el acorde previo se construye sobre la nota que está <strong>cinco grados arriba</strong> de la tonalidad nueva, con 7.</p>

<h2>3. El acorde pivote</h2>
<p>El método más suave. Busca un acorde que pertenezca a <strong>las dos</strong> tonalidades y úsalo como puente. Do mayor y Sol mayor comparten C, Em, G y Am. Si tocas Am, el oído lo escucha como parte de C… y luego lo tratas como parte de G:</p>
<div class="prog"><span>C</span><span>F</span><span>Am</span><span>D7</span><span>G</span><em>Am es el puente, D7 confirma G</em></div>
<p>Este cambio es tan suave que mucha gente no lo nota. Solo siente que la canción se abrió.</p>

<h2>Extra: ve a la relativa menor</h2>
<p>Do mayor y La menor usan exactamente las mismas notas. Llevar tu estrofa a Am (con un E7 antes) te da una sección más oscura sin aprender notas nuevas.</p>
<div class="prog"><span>C</span><span>F</span><span>E7</span><span>Am</span><em>un giro más oscuro</em></div>

<h2>Lista rápida</h2>
<ul>
<li>Elige la tonalidad nueva según el rango de quien canta, no solo según la guitarra.</li>
<li>Prepárala con el V7 de la tonalidad nueva, salvo que quieras un sacudón repentino.</li>
<li>Cambia de tonalidad al empezar una sección, no a mitad de una frase.</li>
<li>Cuando llegues, quédate el tiempo suficiente para que el oído la acepte como casa.</li>
</ul>
''',
try_text='Usa <strong>Cambiar de tonalidad</strong> en Chordseed: elige dónde estás y a dónde quieres ir, y te muestra caminos para llegar, con los acordes puente y pivote marcados, toca cada uno y dibuja el recorrido en el círculo de quintas. Gratis, en tu navegador.')

POSTS_ES['numbers'] = dict(
slug='grados-de-acordes-numeros-romanos', eyebrow='Teoría básica', minutes=7,
title='Los grados de los acordes: toca cualquier canción en cualquier tonalidad',
desc='Qué significan I, IV, V y vi, las familias de acordes de las tonalidades más comunes en guitarra, el sistema de números de Nashville, cómo transportar una progresión y cómo encontrar la tonalidad de una canción.',
card='I, IV, V, vi: el código que usan los músicos para hablar de acordes.',
lede='Cuando un músico dice “es un uno-cuatro-cinco” está usando un código secreto que funciona en todas las tonalidades. Apréndelo una vez y podrás transportar canciones, encontrar su tonalidad y entenderte con cualquier banda.',
alt='Lumen apuntando con su linterna a siete círculos luminosos tallados en un árbol antiguo, uno por cada acorde de la tonalidad',
body='''
<h2>Cada tonalidad tiene una familia de siete acordes</h2>
<p>Toma una escala mayor, arma un acorde sobre cada nota usando solo notas de esa escala, y obtienes siete acordes. Siempre siguen el mismo patrón de mayores y menores:</p>
<table>
<tr><th>Grado</th><th>I</th><th>ii</th><th>iii</th><th>IV</th><th>V</th><th>vi</th><th>vii°</th></tr>
<tr><td>Tipo</td><td>mayor</td><td>menor</td><td>menor</td><td>mayor</td><td>mayor</td><td>menor</td><td>dism.</td></tr>
</table>
<p>Los números romanos en mayúscula son acordes mayores, en minúscula son menores, y el circulito significa disminuido. El patrón nunca cambia; solo cambian los nombres de los acordes.</p>
<p><em>Nota sobre el cifrado:</em> aquí usamos el cifrado americano. C = Do, D = Re, E = Mi, F = Fa, G = Sol, A = La, B = Si.</p>

<h2>Las familias de las tonalidades más comunes</h2>
<table>
<tr><th>Tonalidad</th><th>I</th><th>ii</th><th>iii</th><th>IV</th><th>V</th><th>vi</th></tr>
<tr><td><strong>C</strong></td><td><code>C</code></td><td><code>Dm</code></td><td><code>Em</code></td><td><code>F</code></td><td><code>G</code></td><td><code>Am</code></td></tr>
<tr><td><strong>G</strong></td><td><code>G</code></td><td><code>Am</code></td><td><code>Bm</code></td><td><code>C</code></td><td><code>D</code></td><td><code>Em</code></td></tr>
<tr><td><strong>D</strong></td><td><code>D</code></td><td><code>Em</code></td><td><code>F♯m</code></td><td><code>G</code></td><td><code>A</code></td><td><code>Bm</code></td></tr>
<tr><td><strong>A</strong></td><td><code>A</code></td><td><code>Bm</code></td><td><code>C♯m</code></td><td><code>D</code></td><td><code>E</code></td><td><code>F♯m</code></td></tr>
<tr><td><strong>E</strong></td><td><code>E</code></td><td><code>F♯m</code></td><td><code>G♯m</code></td><td><code>A</code></td><td><code>B</code></td><td><code>C♯m</code></td></tr>
<tr><td><strong>F</strong></td><td><code>F</code></td><td><code>Gm</code></td><td><code>Am</code></td><td><code>B♭</code></td><td><code>C</code></td><td><code>Dm</code></td></tr>
</table>
<p>El acorde vii° no aparece porque casi no se usa en pop y rock.</p>

<h2>Qué hace cada grado</h2>
<ul>
<li><strong>I</strong> es la casa. Las canciones suelen empezar y terminar aquí.</li>
<li><strong>IV</strong> es un paso fuera de casa: abierto y relajado.</li>
<li><strong>V</strong> es la tensión. Quiere volver al I.</li>
<li><strong>vi</strong> es el lado emotivo y menor de la casa.</li>
<li><strong>ii</strong> y <strong>iii</strong> son conectores más suaves que suelen llevar al V o al IV.</li>
</ul>

<h2>Transportar se vuelve fácil</h2>
<p>La famosa progresión I–V–vi–IV es la misma idea en todas las tonalidades. Solo cambian las letras:</p>
<div class="prog"><span>C</span><span>G</span><span>Am</span><span>F</span><em>en C</em></div>
<div class="prog"><span>G</span><span>D</span><span>Em</span><span>C</span><em>en G</em></div>
<div class="prog"><span>D</span><span>A</span><span>Bm</span><span>G</span><em>en D</em></div>
<p>Si una canción te queda muy grave, escríbela en grados, elige una tonalidad más alta y lee las letras nuevas en la tabla. El capo hace lo mismo en la guitarra: con capo en el traste 2, las posiciones de G suenan en tonalidad de A.</p>

<h2>El sistema de números de Nashville</h2>
<p>Los músicos de sesión de Nashville usan la misma idea con números normales: <strong>1 – 5 – 6m – 4</strong>. Así la banda puede seguir una partitura en la tonalidad que pida quien canta, en el momento. Números romanos o de Nashville, es el mismo código.</p>

<h2>Cómo encontrar la tonalidad de una canción</h2>
<ol>
<li><strong>Escucha dónde está la casa.</strong> El acorde que se siente como descanso, normalmente el primero o el último, probablemente es el I.</li>
<li><strong>Revisa la familia.</strong> Busca la fila de la tabla que contiene todos (o casi todos) los acordes de la canción.</li>
<li><strong>Sigue al acorde con 7.</strong> Un acorde como D7 casi siempre apunta a su I, que es G.</li>
<li><strong>¿Mayor o menor?</strong> Si la casa es un acorde menor (por ejemplo Am), la canción está en La menor, que comparte familia con Do mayor.</li>
</ol>
''',
try_text='Pega cualquier progresión en <strong>Analizar mi progresión</strong> en Chordseed. Encuentra la tonalidad, marca cada acorde con su grado y dibuja la curva de tensión para que veas qué hace cada acorde. Gratis, en tu navegador.')

POSTS_ES['lofi'] = dict(
slug='progresiones-de-acordes-lofi', eyebrow='Ánimos', minutes=6,
title='6 progresiones de acordes lo-fi (y por qué suenan tan relajadas)',
desc='Progresiones de acordes de lo-fi hip hop para tocar hoy: acordes con séptima y novena, ciclos ii–V–I y vamps menores, con consejos de tempo, posiciones y swing.',
card='Séptimas, novenas y loops lentos para ese ambiente de madrugada.',
lede='El lo-fi suena relajado y un poco nostálgico, como estudiar de noche con lluvia en la ventana. Casi todo ese ambiente viene de los acordes. Aquí tienes seis progresiones para empezar y las razones por las que funcionan.',
alt='Lumen con audífonos tocando un teclado pequeño en una acogedora casa del árbol de noche, con una taza de té en la mesa',
body='''
<h2>¿Qué hace que unos acordes suenen “lo-fi”?</h2>
<ul>
<li><strong>Séptimas y novenas.</strong> En vez de C o Am a secas, el lo-fi usa Cmaj7, Am9, Dm7. Las notas extra hacen que los acordes suenen suaves y sin resolver.</li>
<li><strong>Loops cortos.</strong> Dos o cuatro acordes que se repiten una y otra vez, para que quien escucha se relaje.</li>
<li><strong>Movimiento de jazz.</strong> Muchos loops toman el ii–V–I del jazz, pero más lento.</li>
<li><strong>Tempo lento con swing.</strong> Normalmente entre 70 y 90 BPM, con una batería que se siente un poco perezosa y atrasada.</li>
</ul>

<h2>1. El loop descendente</h2>
<p>Cada acorde baja un escalón. Se siente como un suspiro lento.</p>
<div class="prog"><span>Fmaj7</span><span>Em7</span><span>Dm7</span><span>Cmaj7</span><em>IV – iii – ii – I en C</em></div>

<h2>2. El ciclo de jazz</h2>
<p>El clásico 1–6–2–5. Nunca se siente terminado, y eso es perfecto para un loop.</p>
<div class="prog"><span>Cmaj7</span><span>Am7</span><span>Dm7</span><span>G7</span><em>I – vi – ii – V</em></div>

<h2>3. El ii–V–I con novenas</h2>
<p>El mismo movimiento de jazz con colores más ricos. Cambia G9 por G13 si lo quieres todavía más soñador.</p>
<div class="prog"><span>Dm9</span><span>G9</span><span>Cmaj9</span><span>Cmaj9</span><em>ii – V – I</em></div>

<h2>4. El vamp menor de dos acordes</h2>
<p>Solo dos acordes, pero con novenas suenan profundos. Ideal para poner melodías o samples encima.</p>
<div class="prog"><span>Am9</span><span>Dm9</span><em>i – iv en La menor</em></div>

<h2>5. El menor agridulce</h2>
<p>El E7 agrega un momento de tensión antes de volver a Am. Melancólico y de película.</p>
<div class="prog"><span>Fmaj7</span><span>E7</span><span>Am7</span><span>Am7</span><em>VI – V – i en La menor</em></div>

<h2>6. El impulso neo-soul</h2>
<p>El A7 no pertenece a la tonalidad de C: es una dominante secundaria que empuja hacia Dm7 y le da al loop un toque soul.</p>
<div class="prog"><span>Cmaj7</span><span>A7</span><span>Dm7</span><span>G7</span><em>I – VI7 – ii – V</em></div>

<h2>Consejos para que suene bien</h2>
<ul>
<li><strong>Toca suave.</strong> Un piano eléctrico o una guitarra limpia y cálida funcionan mejor. Evita rasgueos fuertes.</li>
<li><strong>Usa posiciones cercanas.</strong> Mueve la menor cantidad de dedos posible entre acordes para que el loop fluya.</li>
<li><strong>Deja respirar.</strong> Un acorde por compás, a veces dos compases, es más que suficiente.</li>
<li><strong>Agrega textura.</strong> El ruido de vinilo, la lluvia o el siseo de cinta son parte del género, pero los acordes van primero.</li>
</ul>
''',
try_text='En Chordseed, elige el estilo <strong>Lo-fi hip hop</strong> y un ánimo soñador o melancólico. El generador te sugiere séptimas y novenas relajadas y toca tu loop con un ritmo tranquilo y un bajo detrás. Gratis, en tu navegador.')
