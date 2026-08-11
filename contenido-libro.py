# -*- coding: utf-8 -*-
"""
Content model for "Pequeñas composiciones de una niña".

Every piece of prose and every caption is pulled from the original .docx by
paragraph index, so no text is retyped.  Only three kinds of edit are applied,
all declared explicitly here:
  * paragraphs that the original split mid-sentence to flow around a photo are
    rejoined  ->  P(254, 255)
  * captions that were broken across several paragraphs are merged  ->  cap_p(226,227,228)
  * captions that pointed at a page position ("Foto izq.", "Arriba", "F2")
    lose that prefix, because each photo now carries its own caption
    ->  cap_t(...)  with the surviving words quoted verbatim from the original
"""
import json

PARAS = json.load(open('paras.json'))


# ---------------------------------------------------------------------------
# Correcciones de la autora (agosto 2026), del zip "Correcciones de Pequeñas"
# y del mail. Cada una declara el texto original y el corregido; si el original
# ya no coincide, el build falla en vez de aplicar la correccion a ciegas.
# ---------------------------------------------------------------------------
CORRECCIONES = {
    # -- Mov 1
    65:  [('rep', 'estudiar todos los días piano.', 'estudiar todos los días.')],
    68:  [('add', 'Era la primera que avistaba la llegada del mercachifle (vendedor '
                  'ambulante) que avanzaba en su carreta tirada por un caballo y una mula. '
                  'A veces venían con él un bandoneonista ciego y el peluquero para los peones.')],
    210: [('rep', 'no aceptó el viaje y le regalaron', 'no aceptó el viaje le regalaron')],
    251: [('rep', 'un patio francés con estatuas.',
                  'un patio francés con estatuas cuyas poses imitábamos para sacarnos fotos.')],
    # -- Mov 2
    301: [('rep', 'le pagarle las cuentas', 'le pagaba las cuentas')],
    # -- Mov 5
    388: [('rep', 'hasta el día de hoy, y muy envidiada', 'hasta el día de hoy, muy envidiada')],
    # -- Mov 6
    413: [('rep', 'se habrá enterado de lo sucedido? me pregunté.',
                  'se habrá enterado de lo sucedido, me pregunté.'),
          ('rep', 'en otra etapa de su vida? etc etc,', 'en otra etapa de su vida, etc etc,')],
    426: [('rep', 'yo trato de seguir sus pasos.',
                  'yo trato de seguir sus pasos. Marcelo el parquero de siempre tiene todo '
                  'impecable, lo mismo que Marta en el chalet que cocina como los dioses y '
                  'siempre volvemos con unos quilos de más.')],
    # -- Mov 7
    500: [('rep', 'los yödels que nos había enseñado', 'los yodels que nos había enseñado')],
    # -- Mov 9
    556: [('rep', 'Actualmente me reencontré con mis primos Sastre',
                  'Actualmente me veo más con mis primos Sastre')],
    # -- Lotty va con dos T en todo el libro, no solo en su movimiento
    172: [('rep', 'el padre de Loty y Pedro', 'el padre de Lotty y Pedro')],
    407: [('rep', 'tía Yolanda y Loty mi prima', 'tía Yolanda y Lotty mi prima'),
          ('rep', 'Loty que además era muy amiga', 'Lotty que además era muy amiga')],
    # -- Mov 13
    817: [('rep', 'Mov 13: Loty y Tristezas', 'Mov 13: Lotty y Tristezas')],
    818: [('rep', 'me llamo Loty Inchauspe', 'me llamo Lotty Inchauspe')],
    827: [('rep', 'Loty aparte de escribir', 'Lotty aparte de escribir'),
          ('rep', 'Tristezas por Loty.', 'Tristezas por Lotty.')],
    # -- Mov 14
    845: [('rep', 'Muy muderna para su época.', 'Muy moderna para su época.')],
    # -- Mov 15
    886: [('rep', 'con Mercedes, Silvia y Susana Donatiello',
                  'con Mercedes, Silvia Pieres y Susana Donatiello')],
    # -- Mov 18
    951: [('rep', 'el puntapié inicial Hubieron muchas más.',
                  'el puntapié inicial. Hubieron muchas más.')],
    982: [('rep', 'Yo empecé a aprender a tocar jazz. Tuve un excelente profesor, Tato Turano.',
                  'Yo empecé a estudiar jazz con un excelente profesor, Tato Turano.')],
    983: [('rep', 'él quería que hiciéramos un concierto pero mi pánico escénico me lo impidió.',
                  'Me propuso hacer un concierto pero mi pánico escénico me lo impidió.')],
    988: [('rep', 'que es muy buen guitarrista.', 'que es muy buen guitarrista. También es psicóloga.')],
    # -- Mov 20
    1113:[('rep', 'Hicimos juntas jardines y terrazas,fueron tiempos de mucho trabajo,',
                  'Hicimos toda clase de jardines y terrazas. Fueron tiempos de mucho trabajo,')],
    # -- Finale
    1226:[('rep', 'nos parecemos en tantas cosas, ¡que a veces me sorprende!',
                  'nos parecemos en tantas cosas, que a veces me sorprende.')],
}

def _corregir(n, ls):
    ops = CORRECCIONES.get(n)
    if not ops:
        return ls
    ls = list(ls)
    for op in ops:
        if op[0] == 'rep':
            _, viejo, nuevo = op
            golpes = sum(l.count(viejo) for l in ls)
            assert golpes == 1, (
                f'correccion para el parrafo {n}: esperaba 1 coincidencia de '
                f'{viejo!r}, encontre {golpes}')
            ls = [l.replace(viejo, nuevo) for l in ls]
        elif op[0] == 'add':
            ls.append(op[1])
    return ls

def lines(n):
    return _corregir(n, PARAS[str(n)]['lines'])

def cap_p(*ns):
    """caption text = the given paragraphs, joined"""
    out = []
    for n in ns:
        out.extend(lines(n))
    return ' '.join(out)

def cap_t(text):
    return text

def P(*ns):
    """prose block: one <p> per source line, paragraphs joined in order"""
    out = []
    for n in ns:
        out.extend(lines(n))
    return ('prose', out)

def PL(n, a, b=None):
    """prose from a slice of paragraph n's lines (1-indexed, inclusive)"""
    ls = lines(n)
    return ('prose', ls[a-1:(b if b is not None else a)])

def H2(text):
    return ('h2', text)

def FIG(files, cap=None):
    """one figure: list of image files sharing a single caption (or none)"""
    if isinstance(files, str): files = [files]
    return ('fig', files, cap)

def PAIR(*items):
    """a row of photos, each with its own caption: PAIR((file, cap), (file, cap))"""
    return ('pair', [(f, c) for f, c in items])

def GALLERY(files, cap=None):
    return ('gallery', files, cap)

# ----------------------------------------------------------------------------

DOC = [
    ('title',    'Pequeñas composiciones de una niña'),
    ('subtitle', '(en varios movimientos)'),
    ('byline',   'Margarita Sastre Inchauspe'),
    ('dateline', cap_p(1)),

    FIG('image102.jpg', None),

    P(4), P(5), P(6),

    # ---------------------------------------------------- Mov 1
    H2(cap_p(14)),
    P(16),
    FIG(['image111.jpg', 'image112.jpg'], cap_p(19)),
    P(21),
    P(22),
    FIG('image49.png', cap_p(24)),
    P(26), P(27), P(28), P(29), P(30), P(31),
    FIG('image21.jpg', cap_p(32)),
    P(53),
    FIG(['image5.jpg', 'image12.jpg']),
    P(54), P(55),
    P(56), P(57), P(58),
    FIG('image39.jpg', cap_p(60)),
    P(65), P(67), P(68), P(69), P(70),
    FIG('image100.jpg', None),
    P(71), P(72), P(73), P(74), P(75),

    P(85), P(86),
    FIG('image115.jpg', cap_p(87)),
    FIG('image87.jpg', cap_p(91)),
    P(105), P(106),
    P(114),
    FIG('image101.jpg', cap_p(117)),
    P(130), P(131), P(132),
    FIG('image36.jpg', None),

    P(149),
    FIG('image92.jpg', None),
    FIG('image35.jpg', cap_p(151)),
    P(153),
    PAIR(('image76.jpg', cap_t('Tumba de los Zanoia donde están enterrados mis bisabuelos')),
         ('image103.jpg', cap_t('Palazzo Silva con mis hijas'))),
    P(172),
    FIG('image108.jpg', cap_t('De izq a derecha: arriba, Andrés, Mario, Pedrito, Lito. Abajo, la abuela, Susana, mamá y el abuelo Inchauspe.')),
    P(186),
    PAIR(('image37.jpg', cap_t('El 2do de la izq es el abuelo I')),
         ('image45.jpg', cap_p(194))),
    FIG('image64.jpg', cap_p(197)),
    P(209), P(210),
    FIG('image24.jpg', None),
    P(218), P(219),
    FIG('image62.jpg', None),
    P(223), P(224),
    PAIR(('image105.jpg', cap_t('El abuelo después de ganar una copa en remo, en la 2da fila, segundo de la izqu. El último de la misma fila es Jorge Newbery.')),
         ('image97.jpg', None)),
    P(243),
    FIG('image55.jpg', cap_p(245)),
    P(250), P(251), P(252), P(253), P(254, 255), P(256),
    FIG('image106.jpg', cap_p(257)),
    P(259), P(260), P(261),
    FIG('image65.jpg', cap_p(262)),
    P(263), P(264), P(265), P(266), P(267),
    FIG('image18.jpg', None),
    P(279), P(280), P(281), P(282), P(283), P(284),
    PL(287, 1, 3),
    FIG('image26.jpg', cap_t('De izq a derecha con Eleonora, Marina y Graciela')),
    P(290), P(291),
    FIG('image69.jpg', cap_p(293)),
    FIG('image63.jpg', cap_p(294)),

    # ---------------------------------------------------- Mov 2
    H2(cap_p(298)),
    P(300), P(301), P(302), P(303), P(304), P(305),
    FIG('image48.jpg', None),

    # ---------------------------------------------------- Mov 3
    H2(cap_p(312)),
    P(313),
    FIG('image78.jpg', cap_t('Foto de los peones en la manga, sacada por mí')),
    PAIR(('image117.jpg', cap_t('A caballo')),
         ('image41.jpg', cap_t('En la manga'))),
    FIG('image85.jpg', cap_t('Andando en jeep por la laguna Las Tunas, seca en esa época')),
    P(336), P(337, 338), P(339), P(340), P(341), P(342), P(343),
    FIG('image89.jpg', None),
    P(344), P(345), P(346), P(347), P(348),
    FIG('image118.jpg', cap_p(352)),
    FIG('image114.jpg', cap_p(359)),

    # ---------------------------------------------------- Mov 4
    H2(cap_p(365)),
    P(367), P(368), P(369),

    # ---------------------------------------------------- Mov 5
    H2(cap_p(372)),
    P(374), P(375),
    FIG('image42.jpg', cap_t('De izq a derecha mamá, Miss Mary, María Luisa, Mónica Beccar Varela, yo, Máximo Costela')),
    P(376), P(377), P(378), P(379),
    PAIR(('image10.jpg', cap_t('María Luisa')),
         ('image47.jpg', cap_t('Esquiando, con Memi atrás')),
         ('image83.jpg', cap_t('Mamá tomando sol, aprovechando cada rayito'))),
    P(388), P(389),
    FIG('image93.jpg', cap_p(393)),
    P(395), P(396),

    # ---------------------------------------------------- Mov 6
    H2(cap_p(401)),
    P(403), P(404), P(405), P(406), P(407), P(408), P(409), P(410), P(411),
    P(413), P(414), P(415), P(416), P(417),
    ('h3', cap_p(419)),
    P(421),
    GALLERY(['acuarela-nueva-belgica.jpg', 'image4.jpg', 'image74.png'], cap_p(422)),
    P(424), P(425), P(426),
    PAIR(('image29.jpg', None),
         ('image66.jpg', None)),

    # ---------------------------------------------------- Mov 7
    H2(cap_p(482)),
    FIG('image77.jpg', cap_t('De izq a derecha: Janina Caminos, Ernesto Ezcurra, Anery Aste, Carlos al piano y yo. Atrás, Freddy Arocena, Carlos Sastre, Marcos Arocena y Nora Caminos.')),
    P(493), P(494), P(495),
    FIG('image46.jpg', None),
    P(497), P(498), P(499), P(500, 501), P(502),
    FIG('image38.jpg', None),
    FIG('image43.jpg', cap_t('Con Hebe y Silvia en el camarín de un teatro.')),

    # ---------------------------------------------------- Mov 8
    H2(cap_p(509)),
    P(511), P(512),
    FIG('image28.jpg', cap_p(518)),
    P(514), P(515), P(525), P(526), P(527), P(528), P(529),
    FIG('image16.jpg', cap_t('Foto familiar de cuando ya estábamos todos casados y con hijos. Festejo del triunfo de el Violinista en Palermo: arriba de izq a derecha, Pablos Mayorga, Mita y Gonzalo Villamil, Mario Perkins (h), Nacho y Ceci, Maggie, Chofi e Isa Perkins, Mili Solá. Abajo: yo, Zulema P. De Villamil, Julio Perkins, Luis Villamil, Mario Perkins, Luis Villamil (h) y Luz Quiroga su mujer, Paula Llorente de Villamil.')),

    # ---------------------------------------------------- Mov 9
    H2(cap_p(552)),
    P(553), P(554), P(555), P(556),
    PAIR(('image75.jpg', cap_t('Arriba de izq a derecha, Pancho, Chofi, papá, yo, Mario (h). Abajo Mario Perkins, Saxo, Isa y Maggie.')),
         ('image98.jpg', cap_p(561))),
    FIG('image19.jpg', cap_t('De izq a derecha, Pichi Morelli Sastre y Sra., María Luz y Rafa Martin Grondona Sastre, yo, Cristina, Cecilia y Susy Sastre Gowland.')),
    P(592), P(593), P(594), P(596), P(597),
    FIG('image110.jpg', None),
    PAIR(('image116.jpg', cap_t('Teresa y Don Edmundo')),
         ('image67.jpg', cap_t('Doña Marta y Carlos'))),
    FIG('image71.jpg', cap_t('Flia Perkins en mi casamiento: arriba de izq a derecha, Cacho Pieres, Julio Perkins y Evelyn, Martita Pieres, Malú, María Perkins, Roberto Perkins. Abajo Lucila Pieres, Marta Perkins, Silvia Pieres, Emilia Perkins, Bábela y Edmundo Perkins, Tessy y María Irene Perkins, Mita Villamil, Zulema Perkins y atrás Luis Villamil.')),
    P(610), P(611), P(612), P(613),

    ('h3', cap_p(617)),
    P(618), P(619), P(620),
    FIG('image31.jpg', cap_p(622)),

    ('h3', cap_p(629)),
    FIG('image51.jpg', cap_p(630)),
    P(632), P(633), P(634), P(635), P(636),
    PAIR(('image13.jpg', cap_t('Con Evelyn y Malú')),
         ('image23.jpg', None)),
    P(637),

    ('h3', cap_p(648)),
    FIG('image79.jpg', None),
    P(649), P(650), P(651), P(652), P(653),

    ('h3', cap_p(658)),
    P(660), P(661), P(662), P(663), P(664),
    FIG('image32.png', cap_t('Navidades en la quinta La Rosada con toda la familia Perkins')),

    # ---------------------------------------------------- Mov 10
    H2(cap_p(723)),
    P(725), P(726), P(727), P(728), P(729), P(730), P(731), P(732), P(733), P(734),
    FIG('image50.jpg', cap_t('Foto de Bandi Binder en Punta del Este')),
    FIG('image57.jpg', cap_t('Mis hijos con su bisabuela Inchauspe')),

    # ---------------------------------------------------- Mov 11
    H2(cap_p(741)),
    P(743), P(744), P(745),
    FIG('image99.jpg', cap_t('Arriba Pancho, Mario; abajo, Isa, Chofi y Maggie')),
    FIG('image53.jpg', cap_t('Despedida de Ombú, último día. Arriba Maximo, Mario y Pancho. Rochi, Isa y Delfi. Yo, Hana, Maggie con Sol en brazos. Mary Kelsey, Ruben, Paula y Chofi.')),

    # ---------------------------------------------------- Mov 12
    H2(cap_p(761)),
    P(763), P(764), P(765), P(766),
    FIG('image60.jpg', cap_p(770)),
    FIG('image6.jpg', cap_t('Con los chicos y Mario en Portillo, y nuestro bungalow tapado por la nieve')),
    FIG('image82.jpg', cap_t('En Bariloche con Mario y Rosa María Ricci, Florencia y Hebe Murray y Esteban Azumendi.')),
    PAIR(('image7.jpg', cap_t('Con María Luisa Zorraquín y Hebe en Cumelen')),
         ('image33.jpg', cap_t('Con Nanes Moyano, Silvia Küderli y Hebe en San Martín de Los Andes'))),

    # ---------------------------------------------------- Mov 13
    H2(cap_p(817)),
    P(818), P(819), P(820), P(821), P(822), P(823), P(824), P(825), P(826), P(827),
    PAIR(('image90.jpg', cap_t('El living de Ombú, que era mi cuarto de música')),
         ('image34.jpg', cap_t('Con Loty y Máximo en una exposición de sus obras'))),

    # ---------------------------------------------------- Mov 14
    H2(cap_p(833)),
    P(835), P(836),
    PAIR(('image61.jpg', cap_t('Con Silvia cantando yodels')),
         ('image8.jpg', cap_t('Con Hebe haciéndole el coro a Esteban Azumendi. Atrás Quique Berro y Marcelo O`Reilly'))),
    P(842), P(843), P(844), P(845),

    # ---------------------------------------------------- Mov 15
    H2(cap_p(848)),
    P(850), P(851), P(852),
    FIG('image9.jpg', cap_p(857)),
    P(866), P(867), P(868), P(869),
    P(871), P(872), P(873), P(874), P(875), P(876),
    P(877), P(878), P(879), P(880),
    PAIR(('image107.jpg', cap_t('Con Patricia en Bariloche')),
         ('image113.jpg', cap_t('Patricia y las Arriola'))),
    FIG('image91.jpg', cap_t('La Gorda Pero, patinando en La Barra, Isa y Mario Ricci la sostienen. '
                             'Sentadas Magdalena E. De Inchauspe y Zulema Villamil')),
    P(886), P(887), P(888), P(889),

    # ---------------------------------------------------- Mov 16
    H2(cap_p(891)),
    P(893), P(894), P(895), P(896),
    FIG('image20.jpg', cap_p(892)),

    # ---------------------------------------------------- Mov 17
    H2(cap_p(897)),
    P(899),
    FIG('image11.jpg', cap_p(901)),
    P(908), P(909), P(910), P(911),
    FIG('image68.png', cap_p(906)),
    P(912), P(913), P(914), P(915), P(916), P(917),
    FIG('image3.jpg', cap_t('Con Edith Fischer en el jardín de Ombu.')),

    # ---------------------------------------------------- Mov 18
    H2(cap_p(941)),
    P(943), P(944), P(945),
    FIG('image72.jpg'),
    P(946), P(947), P(948), P(949), P(950), P(951),
    FIG('image17.jpg', None),
    P(982), P(983), P(984), P(985),
    P(986), P(987), P(988), P(989), P(990), P(991),

    # ---------------------------------------------------- Mov 19
    H2(cap_p(1031)),
    P(1033), P(1034), P(1035),
    FIG('image15.jpg', cap_p(1053)),
    P(1058), P(1059), P(1060), P(1061), P(1062), P(1063), P(1064), P(1065),
    GALLERY(['image109.png', 'image104.png', 'image70.png', 'image22.png',
             'image94.jpg', 'image14.png', 'image1.jpg', 'image25.png'],
            None),

    # ---------------------------------------------------- Mov 20
    H2(cap_p(1108)),
    P(1110), P(1111), P(1112), P(1113), P(1114),
    PAIR(('image44.png', cap_t('Con Graciela en plena plantación')),
         ('image40.jpg', cap_t('Parque Micaela Bastida'))),

    # ---------------------------------------------------- Mov 21
    H2(cap_p(1134)),
    P(1136), P(1137), P(1138), P(1139),
    FIG('image58.jpg', None),
    P(1147), P(1148), P(1149),
    FIG('la-pedrera.jpg', cap_t('La casa de La Pedrera, Uruguay')),
    PAIR(('image59.jpg', None),
         ('image96.jpg', None)),
    P(1150), P(1151), P(1152), P(1153),
    FIG('image54.jpg', None),

    # ---------------------------------------------------- Mov 22
    H2(cap_p(1174)),
    P(1176), P(1177), P(1178), P(1179), P(1180), P(1181), P(1182),

    # ---------------------------------------------------- Finale
    H2(cap_p(1186)),
    P(1194), P(1195),
    FIG('image119.png', cap_t('En el Perito Moreno')),
    FIG('image80.png', cap_t('Con Delfi, Maggie, Paula, Chofi, Isa y Beethoven en Bonn')),
    P(1226),
    FIG('image56.jpg', cap_p(1227)),
    P(1229), P(1230),
    FIG('image73.jpg', None),
    P(1231),
    FIG('image81.png', None),
    FIG('image27.jpg', None),
    P(1237),
    FIG('image52.png', cap_p(1251)),
    PAIR(('image86.jpg', None),
         ('image2.jpg', None)),
    PAIR(('image30.png', cap_t('Con mis hijos y Emilia en la terraza de Scalabrini')),
         ('image84.jpg', cap_t('Valparaíso, festejo de mis 80'))),
    FIG('cumple-80-zapallar.jpg', cap_t('Mi cumple de 80 en Zapallar con toda la familia')),
    P(1238),
    ('closing', cap_p(1272)),
    ('sig', 'Margarita Sastre Inchauspe'),
    FIG('image88.jpg', None),
]
