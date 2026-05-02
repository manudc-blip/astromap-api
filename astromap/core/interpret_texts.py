# -*- coding: utf-8 -*-
# Auto-normalized interpretation texts (verbatim) for AstroMap.

INTRO_TEXTS = {
    "FR": {
        "intro": """Les interprétations proposées ici décrivent des tendances psychologiques et comportementales issues du thème de naissance. Pour une lecture pleinement personnalisée, il serait nécessaire de prendre en compte l’ensemble des facteurs extra-astrologiques — éducation, environnement socioculturel, histoire personnelle, hérédité, etc.""",
        "planets": """Chaque planète se définit par un niveau source...
Dans l’analyse astrologique, les planètes constituent généralement l’élément le plus influent du thème, devant les signes zodiacaux puis les maisons astrologiques.""",
        "ret": """En fonction du niveau source (R, E, T) ou du niveau but (r, e, t) des planètes, six familles de trios peuvent être distinguées. Les familles fondées sur un même niveau source sont dites extensives, celles fondées sur un même niveau but sont dites intensives. S’y ajoutent les familles Pouvoir : Extensif (Soleil, Mars, Pluton) et intensif (Lune).
Selon la configuration du thème astrologique, chacune de ces familles peut être dominante, sous-dominante ou non dominante.""",
        "signs": """Le signe zodiacal déterminé par la date de naissance renseigne uniquement sur la position du Soleil au moment de la naissance. Pour identifier les autres signes valorisés dans un thème astrologique, il est nécessaire de considérer la position des autres planètes dans le thème. Ce sont les signes occupés par les planètes qui sont pris en compte dans l’analyse.
Les signes jouent un rôle propre et distinct de celui des planètes dans les tendances psychologiques dont nous héritons à la naissance et qui s’expriment tout au long de la vie. Les planètes s’interprètent à partir des niveaux R, E et T, tandis que les signes expriment une dynamique fondée sur l’alternance diurne et nocturne.""",
    },
    "EN": {
        "intro": """The interpretations presented here describe psychological and behavioral tendencies derived from the natal chart. For a fully personalized reading, it would be necessary to take into account the full range of extra-astrological factors—education, sociocultural environment, personal history, heredity, and so on.""",
        "planets": """Each planet is defined by a source level...
In astrological analysis, planets generally constitute the most influential component of the chart, taking precedence over zodiac signs and then over astrological houses.""",
        "ret": """Depending on the planets’ source level (R, E, T) or goal level (r, e, t), six families of triads can be distinguished. Families based on the same source level are referred to as extensive, while those based on the same goal level are referred to as intensive. Added to these are the Power families: extensive (Sun, Mars, Pluto) and intensive (Moon).
According to the configuration of the natal chart, each of these families may be dominant, sub-dominant, or non-dominant.""",
        "signs": """The zodiac sign determined by the date of birth refers solely to the position of the Sun at the moment of birth. To identify the other signs emphasized in a natal chart, it is necessary to consider the positions of the other planets. In analysis, it is the signs occupied by the planets that are taken into account.
Signs play a role that is distinct from that of the planets in the psychological tendencies we inherit at birth and express throughout life. Planets are interpreted through the R, E, and T levels, whereas signs express a dynamic grounded in the alternation between diurnal and nocturnal phases.""",
    },
}

PLANET_TEXTS = {
    "FR": {
        "p": """Lune « p » (pouvoir intensif : globalité)

Pouvoir intensif :
Vous vous sentez profondément en confiance et paisible, comme enveloppé dans un climat d’abandon serein. Réceptif et accueillant, vous savez créer autour de vous une atmosphère douce et apaisante, faite d’intimité chaleureuse et de convivialité. Vous vous épanouissez dans les environnements familiers et vous adaptez avec souplesse aux besoins et rythmes de vos proches. Vous privilégiez naturellement les solutions fluides face aux problèmes quotidiens.
Rêveur et imaginatif, vous possédez une vie intérieure riche et foisonnante, où vos aspirations à la plénitude, à l’harmonie et à la sérénité occupent une place centrale. Vous vous sentez en parfaite osmose avec vous-même et avec votre environnement, pourvu que celui-ci soit en équilibre avec vos valeurs et en accord avec votre sensibilité profonde.""",

        "rR": """Soleil « rR » (représentation de la Représentation)

Représentation extensive (R) :
Vous ressentez un besoin profond d’être reconnu et admiré d’emblée. Dès que vous entrez en scène, vous souhaitez apparaître comme un être unique, exemplaire, digne d’estime, et accordez un soin extrême à l’image que vous projetez. Pour vous épanouir pleinement, vous recherchez des échanges sociaux intenses, dans lesquels vous aspirez à occuper une position centrale et valorisante. Vous faites tout pour ne pas décevoir les attentes que l’on place en vous.

Représentation intensive (r) :
Vous avez aussi un goût marqué pour la clarté et la précision. Vous vous engagez avec passion et intégrité dans tout ce que vous faites ou exprimez, veillez à garder le contrôle de vous-même, et cherchez à maîtriser ce qui vous entoure. Guidé par des convictions solides, vous poursuivez avec ténacité les objectifs que vous vous êtes fixés, et auxquels vous vous identifiez profondément.""",

        "eR": """Vénus « eR » (existence de la Représentation)

Représentation extensive (R) :
Vous réagissez spontanément par sympathie ou antipathie, attirance ou appréhension, goût ou rejet. Vous êtes en quête de liens affectifs sincères, de relations privilégiées fondées sur un ressenti partagé et une complicité naturelle. Votre sociabilité est tendre, chaleureuse, attachante. Vous savez toucher et séduire par la grâce de vos attitudes, par votre sensibilité et le charme discret de votre présence.

Existence intensive (e) :
Vous êtes aussi un être sensuel, épris de sensations. Vous aimez sentir, toucher, éprouver ce et ceux qui vous entourent. Le monde vous parle à travers vos sens, éveillant en vous mille impressions délicates. Vous cherchez avant tout à goûter la vie dans ce qu’elle offre de beau, de doux et d’émouvant — avec une sensibilité à la fois esthétique et affective.""",

        "tR": """Mercure « tR » (transcendance de la Représentation)

Représentation extensive (R) :
Vous êtes dans un état d’attente détendue, porté par une curiosité naturelle et un esprit d’exploration léger et spontané. À l’aise dans la communication, vous savez vous amuser de tout et prendre plaisir aux échanges. Fondamentalement sociable, vous recherchez la diversité des rencontres et la richesse des contacts. Les autres vous intriguent dans leur singularité, et vous êtes toujours prêt à engager la conversation, simplement pour le plaisir de dialoguer.

Transcendance intensive (t) :
Ouvert à l’inconnu et à l’imprévu, vous vous méfiez des vérités figées et des routines mentales. Vous n’hésitez pas à remettre en question, voire à tourner en dérision, ceux qui prétendent tout savoir. Curieux insatiable, vous multipliez les centres d’intérêt et aimez explorer des domaines toujours nouveaux.""",

        "rE": """Jupiter « rE » (représentation de l’Existence)

Existence extensive (E) :
Vous savez faire preuve d’un pragmatisme structuré et d’un bon sens mesuré dans vos actions comme dans vos paroles. Tourné vers les réalisations concrètes, vous prenez les réalités de l’existence très au sérieux et cherchez à tirer le meilleur parti des opportunités qui se présentent. Entreprenant, vous savez mobiliser votre savoir-faire et votre logique pratique pour aborder les problèmes de manière efficace et dans votre intérêt.

Représentation intensive (r) :
Vous êtes aussi ambitieux et déterminé à atteindre vos objectifs. Vous vous donnez les moyens de vos ambitions et prenez volontiers des initiatives pour coopérer, négocier et construire avec les autres. Doué pour l’organisation, vous avez le sens de la gestion, des talents de pédagogue, de diplomate et de leader.""",

        "eE": """Mars « eE » (existence de l’Existence)

Existence extensive (E) :
Vous êtes franc et spontané dans vos réactions, entreprenant et actif dans votre expérience de vie. Vous explorez les réalités concrètes, vous sentez exister avec intensité et privilégiez ce que vous avez vous-même expérimenté. Dynamique et tenace, vous aimez affronter les faits et agir directement et avec efficacité. Les difficultés ne vous découragent pas, au contraire, elles vous stimulent et renforcent votre détermination.

Existence intensive (e) :
Vous êtes également très sensitif et vivez votre relation au monde à travers chaque fibre de votre corps. Vous agissez et réagissez selon ce que vous ressentez, et votre contact direct avec la réalité vous procure des sensations fortes et authentiques. Vous êtes pleinement vivant et présent dans votre ressenti du moment.""",

        "tE": """Saturne « tE » (transcendance de l’Existence)

Existence extensive (E) :
Vous cherchez le fil invisible qui relie les diverses expériences que vous traversez, sondant les êtres et les choses pour en révéler les profondeurs cachées. Réaliste du long terme, vous êtes patient, prudent et réfléchi : vous n’agissez qu’après avoir étudié toutes les hypothèses et évalué les conséquences de vos actes. Vous prenez du recul face aux situations complexes et aux obstacles rencontrés.

Transcendance intensive (t) :
Vous êtes sagace et profond, toujours en quête d’un ailleurs et de sens. Vous vous détachez facilement des circonstances immédiates pour prendre le temps nécessaire à la réflexion et vous interroger sur des questions existentielles. Sérieux, parfois même pessimiste, vous cultivez une certaine forme d’insatisfaction qui nourrit votre quête intérieure.""",

        "rT": """Uranus « rT » (représentation de la Transcendance)

Transcendance extensive (T) :
Vous savez vous imposer et attirer l’attention grâce à ce que vous considérez comme porteur d’originalité et d’universalité. Votre pensée est incisive et vous affirmez vos certitudes avec force. Vous vous guidez par des motivations profondes, des convictions intimes qui jaillissent du plus profond de vous-même. Vous affirmez votre singularité et votre originalité, simplifiez les problèmes complexes et éclairez ce qui est obscur.

Représentation intensive (r) :
Vous êtes un volontaire intransigeant, pleinement engagé dans des choix qui vous paraissent essentiels. Vous n’hésitez pas à prendre des décisions fermes et définitives, vous investissez toute votre énergie à défendre vos convictions et principes les plus profonds. Vous êtes individualiste, élitiste et inflexible.""",

        "eT": """Neptune « eT » (existence de la Transcendance)

Transcendance extensive (T) :
Vous agissez de manière intuitive, guidé par des pressentiments et des prémonitions, habité par une force qui vous dépasse totalement. Vous êtes un intuitif profondément marqué par les puissances de votre imaginaire et par les réalités subtiles et invisibles que vous percevez intensément. Vos choix s’appuient sur des aspirations profondes, et vous vous laissez porter par votre inspiration, votre instinct et vos intuitions.

Existence intensive (e) :
Vous êtes aussi un être sensible et délicat, qui capte avec intensité les signaux les plus subtils. Vous percevez les moindres variations de l’ambiance autour de vous et réagissez aux humeurs dictées par votre inconscient, souvent changeantes et mystérieuses. Votre vie affective est riche, intense et parfois tumultueuse.""",

        "tT": """Pluton « tT » (transcendance de la Transcendance)

Transcendance extensive (T) :
Vous conservez intacte votre authenticité profonde, impossible à exprimer pleinement par des mots ou des actions. Vous êtes en quête d’une objectivité absolue, ne vous faites d’illusion sur rien ni personne, et vous ressentez un contact direct avec la complexité profonde des êtres et des choses. Énigmatique, vous cultivez vos mystères et vos labyrinthes intérieurs, savez peser subtilement le cours des événements et percevoir leur réalité essentielle.

Transcendance intensive (t) :
Vous êtes aussi un sceptique intégral : rien ne trouve grâce à votre esprit inquisitif et méfiant. Vous êtes toujours convaincu qu’il faut découvrir la dimension cachée des êtres, des choses et des situations. Critique implacable, vous percevez avec une grande acuité ce que les autres dissimulent, consciemment ou non.""",
    },

    "EN": {
        "p": """Moon "p" (intensive power: wholeness)

Intensive power :
You feel deeply at ease and at peace, as if wrapped in a serene atmosphere of gentle surrender. Receptive and welcoming, you naturally create a soft, soothing environment around you—one marked by warmth, intimacy, and conviviality. You flourish in familiar settings and adapt with ease to the needs and rhythms of those close to you. When faced with everyday problems, you instinctively seek the simplest and most fluid solutions.
Dreamy and imaginative, you possess a rich and abundant inner life, where your need for wholeness, harmony, and serenity plays a central role. You feel in perfect harmony with yourself and your surroundings, so long as they remain balanced and aligned with your values and your deep emotional sensitivity.""",

        "rR": """Sun "rR" (representation of Representation)

Extensive representation (R): 
You have a deep need to feel recognized and admired from the outset. As soon as you enter a space, you strive to present yourself as a unique, exemplary, and important individual, paying great attention to the image you project. To truly flourish, you seek intense social interactions where you can occupy a central and valued role. You are careful never to disappoint the expectations placed upon you.

Intensive representation (r): 
You also have a strong appreciation for clarity and precision. You commit wholeheartedly and passionately to everything you do or say, value self-control, and aim to maintain mastery over your environment. Driven by unshakable convictions, you pursue your goals with determination and fully identify with the purpose you’ve set for yourself.""",

        "eR": """Venus "eR" (Existence of Representation)

Extensive representation (R): 
You respond instinctively with sympathy or aversion, desire or apprehension, attraction or distaste. You seek meaningful emotional connections—privileged relationships grounded in shared feelings and natural complicity. Your sociability is tender, warm, and endearing. You know how to touch and charm through the grace of your manner, your sensitivity, and the subtle allure of your presence.

Intensive existence (e):
You are also a sensual being, deeply attuned to physical sensations. You love to feel, to touch, to experience the world and the people around you. The spectacle of life awakens countless impressions within you. You relate to others and to the world primarily through your senses, always in search of aesthetic and emotional pleasure.""",
        "tR": """Mercury "tR" (Transcendence of Representation)

Extensive representation (R): 
You exist in a state of relaxed anticipation, guided by natural curiosity and a light, spontaneous spirit of discovery. Comfortable with communication, you find joy in small things and take genuine pleasure in interaction. Deeply sociable, you seek variety in encounters and richness in human contact. People interest you in all their uniqueness, and you’re always ready to strike up a conversation for the simple enjoyment of dialogue.

Intensive transcendence (t):
Open to the unknown and the unexpected, you’re wary of fixed truths and mental routines. You don’t hesitate to question—or even poke fun at—those who claim to have it all figured out. Endlessly curious, you multiply your interests and love to explore new ideas and unfamiliar territories.""",

        "rE": """Jupiter "rE" (Representation of Existence)

Extensive existence (E): 
You demonstrate structured pragmatism and sound judgment in both your actions and words. Focused on tangible achievements, you take the realities of life seriously and strive to make the most of the opportunities before you. Enterprising, you skillfully apply your know-how and practical logic to address problems effectively and in your best interest.

Intensive representation (e): 
You are also ambitious and determined to reach your goals. You equip yourself with the necessary means to succeed and readily take initiative to cooperate, negotiate, and build relationships with others. Gifted in organization, you possess management skills as well as talents for teaching, diplomacy, and leadership.""",

        "eE": """Mars "eE" (Existence of Existence)

Extensive existence (E): 
You are straightforward and spontaneous in your reactions, proactive and engaged in your life experience. You explore concrete realities, feel your existence intensely, and prioritize what you have personally experienced. Dynamic and persistent, you enjoy confronting facts and acting directly and effectively. Difficulties don’t discourage you; on the contrary, they stimulate you and strengthen your determination.

Intensive existence (e):
You are also highly sensitive, experiencing your connection to the world through every fiber of your body. You act and react based on what you feel, and your direct contact with reality provides you with strong and authentic sensations. You are fully alive and present in your moment-to-moment experience.""",

        "tE": """Saturn "tE" (Transcendence of Existence)

Extensive existence (E): 
You seek the invisible thread that connects the various experiences you go through, probing people and things to uncover their hidden depths. A long-term realist, you are patient, cautious, and thoughtful: you act only after carefully examining all hypotheses and evaluating the consequences of your actions. You take a step back when faced with complex situations and obstacles.

Intensive transcendence (t):
You are insightful and profound, always in search of something beyond and meaningful. You easily detach yourself from immediate circumstances to take the necessary time for reflection and to ponder existential questions. Serious, sometimes even pessimistic, you nurture a certain form of dissatisfaction that fuels your inner quest.""",

        "rT": """Uranus "rT" (Representation of Transcendence)

Extensive transcendance (T): 
You know how to assert yourself and draw attention through what you consider to be original and universally significant. Your thinking is sharp, and you firmly stand by your convictions. You are guided by deep motivations and intimate beliefs that arise from within you. You affirm your uniqueness and originality, simplify complex problems, and bring clarity to what is obscure.

Intensive representation (e):
You are a determined and uncompromising individual, fully committed to choices you deem essential. You do not hesitate to make firm and definitive decisions, investing all your energy in defending your deepest convictions and principles. You are individualistic, elitist, and inflexible.""",

        "eT": """Neptune "eT" (Existence of Transcendence)

Extensive transcendance (T): 
You act intuitively, guided by premonitions and hunches, inhabited by a force that completely transcends you. You are an intuitive person deeply influenced by the powers of your imagination and by subtle, invisible realities that you perceive intensely. Your choices are rooted in profound aspirations, and you allow yourself to be carried by your inspiration, instinct, and intuition.

Intensive existence (e):
You are also a sensitive and delicate being, who keenly picks up on the most subtle signals. You notice the slightest shifts in the atmosphere around you and respond to moods dictated by your unconscious, often changing and mysterious. Your emotional life is rich, intense, and sometimes tumultuous.""",

        "tT": """Pluto "tT" (Transcendence of Transcendence)

Extensive transcendance (T): 
You preserve your deep authenticity intact, one that cannot be fully expressed through words or actions. You seek absolute objectivity, allowing yourself no illusions about anything or anyone, and you feel in direct contact with the profound complexity of beings and things. Enigmatic, you cultivate your mysteries and inner labyrinths, skillfully weighing the course of events and perceiving their essential reality.

Intensive transcendence (t):
You are also a thorough skeptic: nothing escapes the scrutiny of your inquisitive and wary mind. You are always convinced that you must uncover the hidden dimensions of people, things, and situations. As an unrelenting critic, you keenly perceive what others conceal, whether consciously or not.""",
    },
}

RET_FAMILY_TEXTS = {
    "FR": {

        "R": """Famille R – Représentation extensive
(Soleil, Vénus, Mercure)

Vous avez un besoin marqué de reconnaissance et d’échanges sociaux. Vous cherchez à être perçu, apprécié et valorisé dans votre environnement, et accordez une attention particulière à l’image que vous projetez. À l’aise dans les interactions, vous faites preuve de décontraction dans vos attitudes et vous vous imposez naturellement par votre présence, votre charme et votre ouverture d’esprit.
Sociable et accessible, vous êtes spontanément disponible aux sollicitations de votre milieu. Vous appréciez la diversité des contacts et des situations, et trouvez votre équilibre dans la circulation des idées, des relations et des regards portés sur vous.""",

        "E": """Famille E – Existence extensive
(Jupiter, Mars, Saturne)

Vous faites preuve de bon sens, de réalisme et de pragmatisme dans ce que vous entreprenez. Vous accordez une grande importance aux faits concrets et tirez volontiers les leçons de vos expériences, en privilégiant ce que vous avez réellement éprouvé plutôt que les abstractions.
Ancré dans la réalité, vous êtes un homme de terrain, pratique et efficace. Vous abordez la vie de manière directe, prenez les situations à bras-le-corps et n’hésitez pas à vous engager personnellement pour agir, construire et obtenir des résultats tangibles.""",

        "T": """Famille T – Transcendance extensive
(Uranus, Neptune, Pluton)

Vous vous déterminez avant tout à partir de vos intuitions profondes et des mouvements intérieurs qui vous traversent. Vos conduites peuvent parfois sembler imprévisibles, car vous vous fiez davantage à votre instinct qu’aux cadres établis ou aux repères conventionnels. Vous accordez une grande importance à ce qui ne se montre pas immédiatement : le non-dit, le latent, le sous-jacent.
Directement connecté à votre imaginaire, vous êtes attentif à votre inspiration et à ce qui émerge spontanément de vous. Cette sensibilité vous ouvre à une perception élargie du monde et vous confère un fort sens du collectif, des dynamiques globales et des courants qui dépassent l’individu.""",

        "r": """Famille r – Représentation intensive
(Soleil, Jupiter, Uranus)

Vous avez une aptitude marquée à formuler les choses de manière simple, concise et structurée. Vous savez réduire la complexité, schématiser, et recourir à des codes, concepts ou théories pour rendre les idées lisibles, transmissibles et opérantes. Cette capacité vous permet de clarifier, d’organiser et d’imposer des repères de lecture cohérents.
Vous accordez une grande importance à votre position et à votre visibilité publique. Vous vous affirmez volontiers comme une référence ou un modèle de conduite, en défendant des orientations claires et des convictions assumées. Guidé par des objectifs élevés et une ambition affirmée, vous cherchez à incarner ces principes par votre posture, vos choix et vos projets.""",

        "e": """Famille e – Existence intensive
(Vénus, Mars, Neptune)

Vous avez une forte capacité à incarner et à vivre pleinement les désirs qui vous animent. Vous ramenez naturellement votre expérience à ce qu’elle produit comme ressenti émotionnel et comme manifestations concrètes, en privilégiant ce qui est vécu, éprouvé et senti.
Votre rapport au monde passe avant tout par la perception sensorielle, l’intensité des émotions et les élans spontanés. Doté d’un appétit de vivre puissant, vous recherchez des expériences fortes et aimez les partager, dans un souci d’engagement direct et d’authenticité du vécu.""",

        "t": """Famille t – Transcendance intensive
(Mercure, Saturne, Pluton)

Vous avez une aptitude marquée à transformer vos connaissances et vos expériences en interrogations, hypothèses et mises en perspective critiques. Plutôt que de vous satisfaire de réponses établies, vous cherchez à comprendre ce qui se cache derrière les évidences et les certitudes admises.
Sceptique et investigateur, vous partez du principe qu’une partie de l’information reste toujours manquante ou incomplète. Vous enquêtez, analysez et traquez les indices qui permettent d’ouvrir de nouvelles pistes de compréhension, en privilégiant la lucidité, la profondeur et la remise en question des cadres établis.""",

        "p": """Famille p – Pouvoir intensif
(Lune)

Vous avez une aptitude marquée à vous installer dans un état de calme, de confiance et de réceptivité globale. Vous recherchez une continuité intérieure qui vous permet d’intégrer les expériences avec souplesse, en préservant votre équilibre général et votre stabilité de fonctionnement.
Attaché aux environnements familiers, vous développez des liens étroits avec votre entourage et éprouvez un fort besoin d’appartenance et de proximité. Vous privilégiez naturellement l’harmonie, la fluidité des échanges et les formes d’adaptation qui empruntent les voies de moindre résistance au sein de votre milieu.""",

        "P": """Famille P – Pouvoir extensif
(Soleil, Mars, Pluton)

Vous cherchez à conjuguer reconnaissance publique, engagement concret dans la réalité des faits et fidélité à votre propre authenticité. Vous souhaitez exercer une influence à la fois visible, fondée sur votre capacité à vous exprimer, concrète dans l’action sur votre environnement, et plus discrète, agissant en profondeur sur le cours des choses.
Vous ne vous contentez pas d’une seule forme de pouvoir et cherchez à mobiliser plusieurs registres selon les situations. Vous pouvez passer rapidement du discours à l’action, puis à une prise de recul plus lucide, en articulant autorité d’expression, efficacité pratique et sens des valeurs collectives. Cette mobilité élargit votre champ d’influence, tout en pouvant générer des tensions internes dans l’équilibre de ces registres.""",
    },

    "EN": {

        "R": """Family R – Extensive Representation
(Sun, Venus, Mercury)

You have a strong need for recognition and social exchange. You seek to be seen, appreciated, and valued within your environment, and you pay close attention to the image you project. At ease in interactions, you display a relaxed attitude and naturally assert yourself through your presence, charm, and open-mindedness.
Sociable and approachable, you are readily available to the demands of your surroundings. You enjoy a diversity of contacts and situations, and you find balance in the circulation of ideas, relationships, and the attention directed toward you.""",

        "E": """Family E – Extensive Existence
(Jupiter, Mars, Saturn)

You demonstrate common sense, realism, and pragmatism in what you undertake. You place great importance on concrete facts and readily draw lessons from your experiences, favoring what you have directly lived through over abstract considerations.
Grounded in reality, you are a hands-on, practical, and effective person. You approach life directly, tackle situations head-on, and readily commit yourself in order to act, build, and achieve tangible results.""",

        "T": """Family T – Extensive Transcendence
(Uranus, Neptune, Pluto)

You determine your actions primarily through deep intuitions and inner movements that guide you. Your behavior may at times appear unpredictable, as you rely more on instinct than on established frameworks or conventional reference points. You attach great importance to what does not immediately reveal itself—the unspoken, the latent, and the underlying.
Directly connected to your imagination, you remain attentive to your inspiration and to what emerges spontaneously from within you. This sensitivity opens you to a broader perception of the world and gives you a strong sense of the collective, of global dynamics, and of forces that extend beyond the individual.""",

        "r": """Family r – Intensive Representation
(Sun, Jupiter, Uranus)

You have a marked ability to express ideas in a simple, concise, and structured way. You know how to reduce complexity, create clear frameworks, and rely on codes, concepts, or theories to make ideas intelligible, transmissible, and operational. This capacity allows you to clarify, organize, and impose coherent interpretative reference points.
You place great importance on your position and public visibility. You readily assert yourself as a point of reference or a model of conduct, defending clear orientations and well-defined convictions. Guided by ambitious goals and a strong sense of purpose, you seek to embody these principles through your stance, your choices, and your projects.""",

        "e": """Family e – Intensive Existence
(Venus, Mars, Neptune)

You have a strong capacity to embody and fully experience the desires that drive you. You naturally relate your experience to the emotional responses it generates and to its concrete manifestations, giving priority to what is lived, felt, and directly experienced.
Your relationship with the world is shaped primarily by sensory perception, emotional intensity, and spontaneous impulses. Endowed with a powerful appetite for life, you seek intense experiences and enjoy sharing them, driven by a desire for direct engagement and the authenticity of lived experience.""",

        "t": """Family t – Intensive Transcendence
(Mercury, Saturn, Pluto)

You have a marked ability to transform your knowledge and experiences into questions, hypotheses, and critical perspectives. Rather than settling for established answers, you seek to understand what lies behind apparent evidence and accepted certainties.
Skeptical and investigative, you assume that part of the information is always missing or incomplete. You inquire, analyze, and track down clues that open new paths of understanding, favoring lucidity, depth, and the questioning of established frameworks.""",

        "p": """Family p – Intensive Power
(Moon)

You have a marked ability to settle into a state of calm, confidence, and overall receptivity. You seek an inner continuity that allows you to integrate experiences with flexibility, while preserving your general balance and stability of functioning.
Attached to familiar environments, you develop close ties with those around you and experience a strong need for belonging and proximity. You naturally favor harmony, fluid exchanges, and adaptive patterns that follow paths of least resistance within your environment.""",

        "P": """Family P – Extensive Power
(Sun, Mars, Pluton)

You seek to combine public recognition, concrete engagement with the realities of action, and fidelity to your own authenticity. You aim to exercise an influence that is at once visible, grounded in your capacity for expression, concrete in its impact on your environment, and more discreet, operating at a deeper level in shaping the course of events.
You do not limit yourself to a single form of power, but seek to mobilize several registers depending on the situation. You may move quickly from discourse to action, and then to a more lucid step back, articulating authority of expression, practical effectiveness, and a sense of collective values. This mobility broadens your field of influence, while also potentially generating internal tensions in the balance between these different registers.""",
    },
}

SIGN_TEXTS = {
    "FR": {

        "Aries": """Bélier - expression adaptée
Force d’excitation naturelle
En force d’excitation naturelle, l’élan diurne prend le dessus sur l’inertie nocturne, balayant inhibitions et indifférences. L’énergie est intacte, brute, prête à se projeter sans retenue dans l’environnement. Il s’agit d’une agressivité primaire, d’une impulsion pionnière, d’un besoin viscéral de sensations concrètes et brûlantes. La spontanéité est totale, sans à priori : une force instinctive, directe, audacieuse, qui s’exprime généreusement. Il y a un impératif d’action immédiate, qui ne tolère ni attente ni contrainte.

Vitesse d’excitation 
La vitesse d’excitation se manifeste par une mobilisation instantanée de l’énergie disponible : tout démarre au quart de tour, les réponses fusent, les décisions jaillissent. On réagit sur-le-champ, avec des réflexes vifs et une mise en mouvement quasi automatique. Les rythmes sont trépidants, l’auto-accélération sans fin. Cette dynamique nerveuse s’accompagne souvent d’un tempérament cyclothymique et d’une grande réactivité face aux variations du milieu. L’excitation rapide se traduit par un attrait marqué pour les effets saisissants : fanfares, couleurs vives, chocs visuels.

Sens des contraires 
En sens des contraires, dominé par l’intensité et la rapidité de l’excitation, les prises de position sont tranchées, sans nuance ni hésitation : on choisit un camp, et on s’y tient, jusqu’à tomber dans le manichéisme. C’est la franchise brutale, le rejet des compromis, le slogan intérieur : « Avec moi ou contre moi. » Les choix sont instinctifs, impulsifs — mais si l’adaptation l’impose, ces choix peuvent être renversés aussi violemment qu’ils ont été adoptés. Les revirements à 180° ne sont pas rares, avec une ardeur équivalente pour défendre ce qu’on combattait la veille.

Bélier - expression inadaptée
Faiblesse d’inhibition
Incapable de cultiver l’indifférence, de garder son calme ou de prendre du recul, l’impulsif est emporté par l’instant. Il ne sait ni oublier, ni mettre à distance, ni faire le vide : il agit tête baissée, guidé par l’ivresse du moment. Téméraire, impatient, imprévisible, il agit sans calcul ni prudence. Cette difficulté à effacer renforce la puissance des premières impressions, qui s’impriment en lui comme des marques indélébiles. Le manque de recul, et donc de réflexion, l’expose à une forme de crédulité : il peut croire tout et n’importe quoi avec une naïveté désarmante.

Lenteur d’inhibition inadaptée
Quand le frein ne répond plus normalement, deux dérèglements sont possibles. D’un côté, l’incapacité à freiner : l’impulsivité s’emballe, sans limite ni contrôle, créant un état de confrontation continue avec le monde extérieur, une succession d’accidents, de collisions, de débordements. De l’autre, l’incapacité à redémarrer : une fois le frein activé, il reste bloqué. Le sujet s’enferme alors dans des mécanismes de défense rigides, sans nuance ni souplesse. Ses refus deviennent définitifs, ses rancunes persistantes, parfois maladives. Son imaginaire se laisse happer par des univers mythiques, des légendes flamboyantes, souvent déconnectées du réel.

Phase égalitaire
L’agressivité suit ici une trajectoire uniforme, indifférenciée, qui pousse à tout rejeter en bloc. Il n’y a plus de hiérarchie, plus de discernement : tout est mis sur le même plan. L’hostilité devient généralisée, indistincte : les “bonnets blancs et blancs bonnets” sont également condamnés. Ce refus global touche alliés comme adversaires, dans une négation obstinée du bien comme du mal. Aucun dialogue n’est possible, la pensée s’enferme dans une vision personnelle rigide, imperméable à toute remise en question. L’opposition aux contraires se transforme en abstraction totale : un “moi contre tous” sans échappatoire.""",

        "Taurus": """Taureau - expression adaptée
Force d’inhibition
Le Taureau ralentit, se méfie, s’apaise. Il tempère son énergie vitale, apprend à la réguler, à l’économiser. Il impose à sa force un rythme contrôlé, visant la récupération et la stabilité. Il résiste instinctivement à la dispersion, au gaspillage, à l’empressement. Ce retrait volontaire favorise la préservation de l’équilibre psychique et physique. Il sait doser son effort, opposant à l’agitation extérieure une inertie tranquille et ferme.

Induction négative
La Force d’excitation se focalise sur un objet unique, investi de toute l’énergie disponible. Rien d’autre ne compte : concentration exclusive, travail intensif, approfondissement obsessionnel. Il se dévoue sans réserve à un domaine, à un sujet, à une passion, quitte à tomber dans la spécialisation extrême ou la monomanie. Rien ne le détourne de son axe : sa volonté s’incarne dans une fidélité tenace à l’objet de son investissement.

Vitesse d’excitation
Réactif et vif, mais uniquement lorsqu’il est stimulé par l’objet de son Induction. Tant qu’aucun déclencheur pertinent n’intervient, il reste paisible, stable, impassible. Si l’environnement devient trop stimulant, l’adaptation exige un ancrage concret : tenir compte des réalités du terrain pour ne pas se laisser déborder. Si cette adaptation échoue, il peut se réfugier dans un univers abstrait, imaginaire ou idéalisé. Quand l’inhibition cède sous la pression, l’apparente placidité se transforme en tempête : la moindre provocation fait exploser ce qui semblait figé. Dans un équilibre moyen, il sait alterner calme et intensité, savourer les plaisirs sans se nuire : un hédoniste lucide et bon vivant.

Sens des dosages
Le sens des dosages permet de trouver un juste équilibre entre les rejets instinctifs et les compromis nécessaires. L’adaptation s’exerce dans la forme, sans renier le fond. On négocie avec habileté, mais sans perdre de vue son intérêt concret. L’ouverture à l’autre est possible, mais filtrée par la prudence. Face à l’adversité, on préfère la stratégie au conflit direct. Les compromis ne sont jamais une fin en soi, mais un moyen de poser les bases d’un pouvoir solide et durable.

Taureau - expression inadaptée
Faiblesse d’excitation
Le monde ne le surprend plus : il n’attend rien de nouveau, ne perçoit rien de changeant. Éteint à l’avance, paresseux, engourdi, il est insensible à la nouveauté, réfractaire à toute transformation. Il vit replié sur ses expériences passées, ses certitudes, ses jugements figés. Il ne rêve plus, n’imagine plus, n’espère plus : tout est figé, invariable, condamné à se répéter. Il se laisse porter par la routine, en faisant le strict minimum.

Lenteur d’inhibition inadaptée
Il est résolument fermé. L’inertie d’inhibition ne fait que renforcer l’apathie : le frein reste constamment enclenché. Rien ne le pousse à sortir de lui-même. Individualiste radical, peu sociable, il se replie dans un isolement rigide. Il devient sec, dur, doctrinaire, intransigeant. La méfiance devient son réflexe par défaut, la communication se ferme, et la volonté se transforme en refus obstiné. Son intuition s’éloigne des normes, générant des constructions mentales déconnectées, hermétiques, parfois schizoidales. Il érige autour de lui un mur de béton.

Phase paradoxale
Ayant perdu le Sens des intensités, il réagit de façon excessive à des signaux insignifiants. Il lit des intentions cachées là où tout est limpide, s’épuise pour des détails, accorde une importance énorme à des vétilles. Il survalorise le minuscule, l’imperceptible, le marginal. Chez les plus riches de potentiel, cela peut mener à des découvertes insoupçonnées. Chez d’autres, cela débouche sur une susceptibilité exacerbée, une paranoïa chronique. L’énergie est alors entièrement absorbée par l’objet de l’Induction, au détriment du reste du monde : on s’épuise pour une idée fixe, on néglige tout le reste.""",

        "Gemini": """Gémeaux - expression adaptée
Force d’excitation
Chez le Gémeaux, la Force d’excitation a gagné en finesse. Elle se diffuse en une énergie légère, mobile, ouverte à tout. L’esprit papillonne avec curiosité, avide d’explorer les mille facettes du monde. Centres d’intérêt multiples, curiosité éveillée, appétit pour la nouveauté, les apparences, l’abstraction, les jeux d’idées. Grande disponibilité intérieure : tout l’intéresse, tout l’intrigue, tout mérite d’être écouté, regardé, testé. L’adaptabilité passe par la diversité des expériences et la variété des points de vue.

Vitesse d’excitation
À son apogée. Les réactions sont vives, immédiates, flexibles. Le Gémeaux se déplace mentalement et physiquement avec aisance, s’adapte sans effort à l’imprévu, au changement, au mouvement. Il butine d’un objet à l’autre, multiplie les contacts, saisit les opportunités volatiles. Polyvalent, léger, joueur, il excelle dans l’art des transitions rapides, des associations inattendues, des changements de registre. C’est un esprit agile, subtil, inventif, toujours prêt à rebondir.

Sens des ensembles
L’inhibition étant minimisée, rien ne s’oppose à la rencontre des contraires. Le Gémeaux laisse les éléments les plus hétérogènes se croiser, se juxtaposer, se combiner. Il perçoit intuitivement les dynamiques d’ensemble qui relient les fragments les plus disjoints. Tout est échange, tout est relation. Il fait dialoguer les différences sans chercher à les fondre : l’universalité naît du respect des singularités. Humaniste instinctif, médiateur fluide, il favorise l’intelligence collective par sa souplesse, son humour, son sens des nuances.

Gémeaux - expression inadaptée
Faiblesse d’inhibition extinctive
Plus aucun filtre, plus aucune retenue. L’énergie se disperse sans direction ni centre. Le Gémeaux devient volage, futile, léger au point de perdre toute consistance. Il survole tout sans jamais s’arrêter, incapable de se concentrer, de creuser, de s’engager. Facilement influençable, il se laisse modeler par plus fort que lui, devient le jouet naïf des circonstances. Ses réactions sont immédiates, irréfléchies, dictées par le moment. Un courant d’air mental.

Lenteur d’inhibition
Deux versants s’opposent : soit l’inhibition est absente, et le Gémeaux devient une girouette incontrôlable, nerveux, incohérent, en proie à une agitation mentale constante. L’instabilité domine, avec une incapacité à tenir un cap. Soit l’inhibition est figée, impossible à desserrer, et l’intelligence se replie dans un monde abstrait, intellectuel, coupé du réel. Le Gémeaux se réfugie dans une tour d’ivoire théorique, froide et déconnectée, ou bien dans une indifférence nihiliste, désenchantée. Dans les deux cas, la relation au monde est rompue.

Phase ultraparadoxale
Le système s’inverse : ce qui devrait freiner excite, ce qui devrait faire peur attire. Le Gémeaux joue avec les tabous, explore l’interdit, se délecte de l’absurde et du paradoxal. Il se dédouble, imite, parodie, emprunte les masques les plus inattendus. L’identité devient mouvante, floue, perméable. Il se met à la place de l’autre, jusqu’à s’y perdre. Quand l’agilité mentale reste maîtrisée, cela donne un virtuose de la médiation, capable d’allier l’inconciliable. Mais sans repères solides, c’est le grand écart permanent, la fuite dans l’illusion, les contorsions mentales pour justifier l’injustifiable.""",

        "Cancer": """Cancer - expression adaptée
Force d’inhibition
Le Cancer trace des frontières pour se protéger de l’excès de stimulations. Il délimite son espace vital, son pouvoir d’action, son univers intime. À l’intérieur de ce périmètre sécurisé, il explore ses acquis, fait l’inventaire de ses richesses mentales ou affectives, et renforce ses remparts protecteurs. Il défend son cocon, son fief, sa communauté de base. C’est là qu’il se confronte à lui-même : estime de soi, subjectivité, rapport au passé et à l’intime deviennent des enjeux essentiels.

Lenteur d’excitation
L’élan vers l’action est lent, mais constant. Le Cancer avance à petits pas, construit patiemment, organise méthodiquement. Il s’ouvre au monde extérieur avec prudence et maîtrise, dans un souci d’efficacité. Il cherche à tout contrôler dans son environnement immédiat. Les habitudes, les routines, les repères familiers donnent un cadre solide à ses pensées, ses actes et ses émotions. Il conserve, protège, perpétue : les souvenirs, les traditions, les valeurs sont des ancrages durables.

Sens des ensembles
Le monde diurne domine encore, mais décroît : il ne s’agit plus de recevoir, mais d’intégrer. Le Cancer synthétise en milieu clos, absorbe le maximum de contenu dans un cadre défini. Il rassemble, centralise, homogénéise. Il veut garder la mémoire de tout, vivre à fond les multiples dimensions de son monde intérieur et les protéger de toute intrusion. C’est une force de cohérence, de fidélité, de stabilité, capable de porter de nombreux projets dans une même dynamique de fond.

Cancer - expression inadaptée
Faiblesse d’excitation associative
Le Cancer ne veut plus ou ne peut plus s’associer au monde extérieur. Il se replie frileusement dans son cocon, coupe les ponts, ferme toutes les issues. Plus de contact, plus d’ouverture : il pantoufle, se laisse aller, s’abandonne à la paresse ou à l’autosuffisance. Il devient ours, asocial, hermétique, cultivateur de clocher, indifférent aux idées qui ne sont pas les siennes. Il tourne en boucle dans son propre système émotionnel ou mental, s’auto-intoxiquant de ses certitudes ou de ses peurs.

Vitesse d’inhibition inadaptée
Les réactions d’inhibition sont vives mais inappropriées. Le Cancer fuit devant des menaces imaginaires, se défend trop tôt ou à contretemps, s’enferme dans l’évitement. Il s’affole, s’angoisse, panique sans raison claire. Il vit toute intrusion comme un danger. Les mécanismes de sélection s’emballent, les doutes deviennent paralysants, les choix impossibles. Tout ce qui vient de l’extérieur est vécu comme potentiellement hostile.

Phase ultraparadoxale
Les frontières deviennent floues : suis-je dedans ou dehors ? Le casanier rêve d’aventures, le nomade cherche un nid. Réel et imaginaire s’entrelacent, subjectif et objectif se confondent. On s’émeut de ses propres émotions, on pense ses pensées en boucle. Tout s’entasse sans cohérence : bric-à-brac affectif, désordre mental, accumulation de fragments sans fil conducteur. On s’identifie à ce qui rassure (la famille, le lieu, l’autorité), tout en fuyant les mains tendues, les coopérations, les sorties de soi.""",

        "Leo": """Lion - expression adaptée
Force d’excitation débloquante
Le Lion ne supporte ni les carcans, ni les enfermements. Il réagit avec force à toute contrainte : il veut se libérer, se dépasser, briser ses chaînes, sortir des limites, triompher des blocages. C’est l’élan du conquérant, du héros qui s’émancipe de toute tutelle et s’élève au-dessus des obstacles. Il agit avec audace, volonté, orgueil constructif. Il veut rayonner, étendre son influence, affirmer son pouvoir et sa liberté.

Induction positive
Le Lion protège farouchement ce qui est au cœur de son être. En concentrant son énergie protectrice sur ce noyau vital, il se rend invulnérable. Cette sécurité intérieure lui permet ensuite de s’élancer avec panache. Il donne, il rayonne, il dirige — sans crainte de se perdre. Un égocentrisme assumé, mais tourné vers la grandeur : générosité, noblesse, capacité à inspirer les autres.

Lenteur d’excitation
Rien n’est précipité : le Lion agit avec méthode, contrôle et détermination. Il veut bâtir dans la durée, solidifier ses conquêtes, structurer son autorité. Ses passions sont puissantes mais maîtrisées, ses objectifs ambitieux mais réfléchis. Il avance pas à pas, avec une volonté de maîtrise totale sur soi et sur son environnement. Sa puissance repose sur une immense force d’organisation et une ténacité sans faille.

Sens des dosages
Le Lion apprend à équilibrer pouvoir et liberté, autorité et bienveillance, ambition personnelle et intérêt collectif. Il sait composer : ménager ses adversaires pour mieux les vaincre, accorder une marge d'autonomie à autrui pour mieux en tirer profit. C’est l’art de dominer sans asservir, de guider sans brider. Mais à force de compromis, le sens des ensembles peut s’effacer, laissant place à une habile gestion des contraires. Cette « politique de la corde longue » lui permet de garder la main tout en donnant l’illusion de la liberté.

Lion – expression inadaptée
Faiblesse d’inhibition différentielle
Sans finesse ni subtilité, le Lion inadapté s’impose de manière brutale. Il manque de tact, de nuance, de discernement. C’est l’éléphant dans le magasin de porcelaine : il agit sans précaution, dit tout haut ce qu’il devrait taire, envahit l’espace sans se soucier des autres. Incapable de diplomatie, il se montre simpliste, téméraire, souvent maladroit — voire carrément inadapté aux subtilités des rapports humains.

Vitesse d’inhibition inadaptée
Il vit dans l’angoisse de perdre son pouvoir, sa liberté ou son image héroïque. Une blessure à son orgueil réel ou imaginaire peut le paralyser ou le faire paniquer. Il se lance parfois dans des initiatives grandioses qu’il abandonne aussitôt par peur d’échouer. Bluff, fuite en avant ou retrait honteux : il réagit de manière excessive et désordonnée dès qu’il se sent menacé dans son aura personnelle.

Phase paradoxale
Face aux vrais dangers, il reste souvent indifférent. Mais qu’on effleure son ego, et le voilà prêt à tout renverser. Une remarque déplacée, une critique à peine voilée peuvent déclencher chez lui des tempêtes émotionnelles. Il surestime ses forces, sous-estime les obstacles, s’enflamme pour des exploits tapageurs mais néglige les réalités concrètes. Trop préoccupé par son image de vainqueur, il devient vulnérable aux manœuvres plus subtiles : il risque de voir ses triomphes subtilisés par ceux qui savent mieux jouer des apparences.""",

        "Virgo": """Vierge – Expression adaptée
Force d’inhibition bloquante
Chez la Vierge, le frein est fermement enclenché : la protection est précise, ciblée, systématique. Ce repli maîtrisé permet une efficacité concrète renforcée. On renonce à l’inatteignable, on aménage des marges de sécurité, des solutions de repli. L’objectif est la maîtrise de soi et de son environnement : ne rien laisser passer, ne se laisser envahir par rien ni personne. On se prémunit avec prudence et minutie, dans une logique d’autonomie et de prévoyance.

Lenteur d’excitation
L’action est méthodique, lente mais sûre, structurée selon un ordre rigoureux. Rien n’est laissé au hasard. L’efficacité se construit dans la discrétion, par une persévérance silencieuse et implacable. On optimise les moyens, on ritualise les habitudes, on organise l’espace et le quotidien pour en faire un univers fonctionnel et maîtrisé. Le sérieux, la patience, la rigueur deviennent les piliers d’une progression certaine, sans fanfare.

Sens des contraires
La Vierge perçoit avec une extrême acuité les lignes de démarcation : entre soi et les autres, entre le permis et l’interdit, le propre et le sale, le juste et le fautif. Cette claire perception des incompatibilités structure son approche du monde. Rien ne doit se mélanger : on trie, on classe, on segmente. Cette sélectivité peut aller jusqu’à adopter un masque opposé à sa nature profonde pour mieux se protéger. L’intégrité personnelle est une priorité, quitte à se montrer austère, distant ou critique.

Vierge – Expression inadaptée
Faiblesse d’excitation associative
Dans sa version inadaptée, la Vierge se ferme entièrement au monde. Aucun élan, aucune envie de se relier, de partager, de se confronter à l’altérité. Tout est repli sur soi, enfermement dans un univers intérieur fragmenté, morcelé. L’autoprotection devient excessive, interdisant toute audace, toute liberté, toute initiative. Cela peut mener à des complexes d’infériorité, à un manque de vitalité affective, à un isolement douloureux, voire pathologique.

Vitesse d’inhibition inadaptée
La peur devient un réflexe permanent, déconnecté des circonstances réelles. La moindre situation déclenche un réflexe de repli, une crainte incontrôlée : peur de l’autre, du conflit, de l’échec, du jugement. L’angoisse diffuse devient un mode de vie, parfois jusqu’à la névrose. Pourtant, cette inhibition rapide peut parfois masquer des désirs dissimulés ou une quête intérieure de courage, exprimée à travers l’ironie, la mise à distance ou la critique subtile.

Phase égalitaire – choc des contraires
À mesure que le jour et la nuit tendent à s’équilibrer, la Vierge inadaptée devient hypersensible aux oppositions, tiraillée entre les pôles contraires : désir contre devoir, Moi contre l’Autre, licite contre interdit. Ces tensions sont vécues comme des dilemmes paralysants. La recherche d’équilibre vire à la crispation : on devient méfiant par principe, anxieux quoi qu’il arrive. Cela peut conduire soit à un repli autoprotecteur rigide, soit à une hostilité envers l’autre généralisée, jusqu’au sectarisme, à l’exclusion — y compris vis-à-vis de ses proches.""",

        "Libra": """Balance – Expression adaptée
Force d’excitation associative
Avec la fin du monde diurne de l’été, l’énergie de la Balance marque l’entrée dans le nocturne : on se détourne de soi pour s’ouvrir à l’autre, pour rencontrer le monde extérieur dans une relation d’égal à égal. C’est le temps du lien, de l’échange, du dialogue, de la cohabitation harmonieuse avec son environnement perçu comme partenaire. L’esprit cherche à relier, à concilier, à lisser les aspérités. On va vers l’autre avec diplomatie, sens du compromis, en dépassant les oppositions.

Vitesse d’inhibition
Les réactions de défense sont rapides, souples, adaptées : la peur ne paralyse pas, elle est maîtrisée et contournée. On apprend à naviguer avec finesse dans les interactions sociales, à éviter les confrontations directes, à jouer des codes sociaux – politesse, élégance, art du langage – pour canaliser les tensions. La pensée fonctionne par distinctions fines, par analyses nuancées. Avec le sens des contraires, naît une capacité d’arbitrage, une recherche constante d’équilibre et d’harmonie.

Sens des contraires
La Balance ne choisit pas de façon tranchée : elle associe les contraires, compare, pèse, jauge, met en regard les opposés pour en tirer un compromis éclairé. Chaque option est vue comme le complémentaire de l’autre, et non comme son ennemi. Cette posture engendre parfois de l’indécision, des dilemmes profonds, mais aussi une richesse intellectuelle singulière. Le désir d’équité, la crainte de se tromper ou d’exclure poussent à une réflexion raffinée et complexe.

Balance – Expression inadaptée
Faiblesse d’inhibition bloquante
Tout cadre, toute limite, toute contrainte sont refusés : la Balance inadaptée sombre dans un universalisme naïf, s’expose à tous les risques sans discernement. C’est le “laisser-aller” total, la fuite en avant vers toutes les expériences sans filtre. L’absence de discipline mène au désordre, à une liberté qui n’est plus structurante mais dissolvante. Plus de règles, plus de fondations : on ne protège ni ne construit rien de durable, on rejette toute forme d’engagement.

Lenteur d’excitation inadaptée
Le besoin d’organisation et de maîtrise s’exerce à vide : on persévère dans des efforts imaginaires, des illusions grandioses, des fantasmes de toute-puissance. Le monde réel se dissout au profit de châteaux de sable, de causes sans objet, de combats vains contre des ennemis fantasmés. On s’attarde dans le romantisme vague, dans l’illusion métaphysique de sa toute-puissance ou dans l’orgueil de ne pas s’engager.

Phase égalitaire
Tout se vaut, rien ne se distingue : on refuse de choisir, on veut plaire à tout le monde, fréquenter tous les milieux sans jamais prendre position. Cette ouverture systématique tourne à la compromission. On arrondit tous les angles, même quand il faudrait trancher. L’indécision devient indifférence, et le souci de concilier peut dégénérer en opportunisme. On finit par refléter servilement son époque ou son entourage, au détriment de toute authenticité personnelle.""",

        "Scorpio": """Scorpion – Expression adaptée
Force d’inhibition différentielle
Le Scorpion perçoit d’abord ce qui distingue, sépare, tranche : il dissèque, analyse, discrimine, traque les moindres différences. Il se méfie des rapprochements trop faciles et préfère souligner ce qui oppose : chercher la faille, attiser les tensions, approfondir les clivages, marquer sa singularité. Ce sens aigu du discernement l’amène à creuser les contrastes et à explorer les zones de rupture avec précision et lucidité.

Induction négative
Son excitation associative est concentrée, exclusive, presque fusionnelle. Il privilégie les alliances intenses et fermées, les engagements profonds, les serments indéfectibles. Sa perception est focalisée sur les détails, les failles d’un accord, les subtilités d’une relation. Il vit chaque instant avec intensité, comme s’il était chargé d’un enjeu crucial ou d’une portée historique.

Vitesse d’inhibition
Le Scorpion est un inhibé ultra-réactif, passé maître dans l’art de l’esquive intelligente. Il se faufile avec habileté, rusé et agile, entre les pièges et les situations périlleuses. Sa pensée est perçante : elle capte rapidement les coulisses du réel, les intentions cachées. Il manie aussi bien la menace voilée que la promesse ambigüe, sachant rester ferme sur le fond tout en adoptant des formes souples et adaptatives.

Sens des dosages
Chez le Scorpion adapté, le goût du contraste s’allie à une volonté d’unité : il sait marier les opposés dans une vision cohérente. Il joue avec les tensions pour mieux les intégrer, use du double-jeu comme stratégie sans jamais perdre le fil d’un but clair. Dialoguer avec l’adversaire pour mieux le comprendre — ou le dominer — pactiser sans se trahir : il agit aux frontières, dans les zones de fracture, où l’intensité relationnelle est maximale et le contrôle stratégique affiné.

Scorpion – Expression inadaptée
Faiblesse d’excitation débloquante
Replié sur lui-même, enfermé dans sa singularité, le Scorpion inadapté ne parvient plus à se dépasser ni à s’ouvrir. Il s’enlise dans un univers clos, sombre, stagnant : marasme affectif, cadre oppressant, fatalité subie. Il s’attache à ses douleurs, ses échecs, ses failles, jusqu’à s’y complaire, comme pour prouver qu’il reste fidèle à lui-même, fût-ce dans la souffrance. Il tourne en rond dans la prison de son identité blessée.

Lenteur d’excitation inadaptée
Obsédé par ses représentations internes, il s’enferme dans un besoin pathologique de contrôle en milieu clos. Il se croit porteur d’un pouvoir secret, unique, presque magique. Sa rigidité devient source d’arrogance, de refus systématique, d’oppositions stériles. Il agit dans l’ombre, manipule, parasite les autres avec cynisme, tirant profit de leur faiblesse ou de leur souffrance, dans une logique de domination froide et impitoyable.

Phase paradoxale
Perdant le sens des priorités, le Scorpion sur-réagit à des signaux mineurs. Son esprit hyper-analytique se focalise sur ce qui est caché, tabou, marginal — qu’il soit réel ou fantasmé. Il cultive le mystère, la menace à peine voilée, le sous-entendu inquiétant. Sa fascination pour l’obscur pousse à la manipulation : chantage, insinuations, stratégies tordues. Il dramatise à l’excès, noircit tout, devient oiseau de mauvais augure. Dans les cas extrêmes, il cherche à tout contrôler en tirant les ficelles dans l’ombre, au prix de toutes les manœuvres et compromissions.""",

        "Sagittarius": """Sagittaire – Expression adaptée
Force d’excitation associative
Le Sagittaire excelle dans l’art de relier, d’associer, de faire dialoguer les domaines les plus éloignés. Il voit des ponts là où d’autres ne perçoivent que des frontières. Sa sensibilité aux interconnexions l’oriente vers une compréhension globale, presque cosmique, du monde. Il se fond dans le collectif, devient un relais, un vecteur de coopération à grande échelle. Son altruisme actif et chaleureux le pousse à se dépasser pour servir une cause universelle, bien au-delà des intérêts individuels ou partisans.

Vitesse d’inhibition
Il déploie un art consommé de l’esquive subtile et du contournement élégant. Maître des codes sociaux, il sait quand intervenir ou se retirer, s’adapter sans se compromettre. Il prône l’ouverture, l’inclusion, mais sans naïveté : son discernement introduit une forme d’élitisme éclairé. Il imagine des collaborations infinies mais sait, dans la réalité, choisir avec soin ses interlocuteurs et partenaires.

Sens des ensembles
Le Sagittaire cherche à construire une synthèse vaste, fluide, intégratrice. Tout est relié : les détails comme les grandes lignes, le proche et le lointain, le matériel et le spirituel. Son esprit embrasse les totalités — encyclopédique, cosmopolite, universaliste — dans une vision cohérente et dynamique. Il cherche à harmoniser toutes les facettes de l’être en une grande architecture vivante, ouverte aux brassages et aux métissages. Sa pensée surplombe les dualismes et embrasse l’unité dans la diversité.

Sagittaire – Expression inadaptée
Faiblesse d’inhibition bloquante
Le Sagittaire inadapté rejette toute contrainte, toute limite : il ne supporte ni cadre, ni norme, ni règle. Téméraire, imprudent, impatient, il se lance dans toutes les démesures, rêve d’impossible, court après l’absolu. Il brûle ses réserves en quête d’une liberté fantasmatique. Sa volonté de dépassement vire à la fuite en avant, sans ancrage ni prudence. L’instinct de conservation est aux abonnés absents : il veut franchir les limites non pour les repousser, mais pour les nier.

Lenteur d’excitation inadaptée
Son besoin d’organisation se projette sur des ambitions disproportionnées : il lui faut du grandiose, de l’épique, du spectaculaire. L’imagination s’emballe dans un délire de grandeur, une mythomanie qui confine parfois à l’hallucination. Il se voit héros, prophète ou sauveur, mais ce masque de solennité cache souvent un vide intérieur, une incapacité à structurer un projet viable. Il rêve d’horizons lointains sans jamais poser les fondations concrètes qui permettraient de s’y diriger.

Phase ultraparadoxale
Le Sagittaire perd le sens des limites au point de vouloir réconcilier l’irréconciliable. Il tente de faire coexister les visions les plus opposées dans un grand mélange incohérent. Ce qui devrait inquiéter l’excite : il flirte avec le danger, s’amuse à jouer avec le feu, prend des paris absurdes. Il prône l’originalité tout en restant prisonnier de conditionnements sociaux forts : c’est le rebelle de salon, l’anticonformiste convenu. À force de croire qu’un loup peut devenir un agneau s’il est bien reçu, il finit par saborder ses propres principes au nom d’un idéalisme mal dirigé.""",

        "Capricorn": """Capricorne – Expression adaptée
Force d’inhibition extinctive
Le Capricorne évolue dans un monde intériorisé, tourné vers l’essentiel. Il sait faire le tri, couper les ponts avec le superficiel, se détacher des stimulations extérieures pour se concentrer sur ce qui compte vraiment. Froid, impassible, parfois même glacial, il reste inébranlable face aux agitations du quotidien. Il incarne la force du détachement, de l’oubli volontaire, du renoncement stratégique. Ce n’est pas du désintérêt : c’est une fidélité absolue à ce qu’il estime fondamental.

Lenteur d’inhibition
Ses réactions sont lentes mais solides. Il s’installe dans la durée avec endurance et détermination. Il avance lentement, mais sûrement, protégé par des principes rigides et une discipline de fer. Rien ne l’ébranle facilement : sa carapace le rend imperméable aux fluctuations extérieures. Rigueur, patience, stratégie, sens du temps long, goût de l’épure et de la méthode : tout est construit pour durer. Il développe une intuition profonde des structures invisibles, des logiques souterraines.

Sens des ensembles
Le Capricorne cherche à comprendre les fondements, les lois internes, les architectures profondes du monde. Il vise une cohérence parfaite, une organisation où chaque élément trouve sa place. Il ne se contente pas de relier : il articule, structure, assemble avec une extrême précision. Pour lui, chacun doit jouer son rôle dans un ordre plus vaste, où rien ne dépasse. C’est un humanisme de l’ordre : si chacun est un rouage bien ajusté, alors le tout fonctionne harmonieusement. Intégrité, rigueur, fidélité à des principes élevés guident son action.

Capricorne – Expression inadaptée
Faiblesse d’excitation naturelle
Quand le Capricorne se désadapte, il perd toute spontanéité. Plus d’élan, plus de désir, plus d’initiative. Il se replie sur lui-même, s’éteint, s’efface. Il doute de sa valeur, se sent impuissant, incapable de répondre aux sollicitations du monde. Tout devient effort. Il s’enferme dans une inertie morne, sans affects ni envie, comme muré dans une fatigue existentielle. Rien ne le touche, rien ne le motive. Il devient inexpressif, inaccessible, isolé.

Vitesse d’excitation inadaptée
Il a du mal à se mettre en mouvement : soit il reste figé, comme paralysé, rongé par une agitation intérieure qu’il ne parvient pas à exprimer ; soit il s’active de manière erratique, dans des impulsions aussi soudaines qu’inconsistantes. Des sursauts d’excitation sans but réel, des caprices passagers, des humeurs instables qui retombent vite dans une apathie profonde. Il oscille entre immobilisme et agitation stérile, sans trouver de rythme ni de cohérence.

Phase ultraparadoxale
Ce qui devrait stimuler l’effraie. L’ouverture, la nouveauté, le changement deviennent des sources d’angoisse. Même les meilleures nouvelles glissent sur lui sans effet. Il s’accroche à ses habitudes avec une rigidité caricaturale, même lorsque la situation exige réactivité et souplesse. Il rejette ce qu’il désire en secret, méprise ce qu’il n’a pas tout en le convoitant ardemment. Il peut se fondre entièrement dans une cause, une loi, une morale absolue, jusqu’à l’oubli total de soi. Fanatisme froid, sacrifice aveugle au nom d’un idéal sacralisé : il devient l’exécutant impitoyable d’une mission intérieure, prêt à tout, même à l’inhumain, pour rester fidèle à ce qu’il croit être l’essentiel.""",

        "Aquarius": """Verseau - expression adaptée
Force d’excitation recréatrice
Le Verseau ne se résigne jamais. Face à l’usure, à l’ennui ou au désespoir, il oppose une énergie de renouveau. Il régénère, réinvente, ravive : son moteur intérieur pousse à voir les choses autrement, à dépoussiérer les idées reçues, à explorer des angles inédits. Rien n’est jamais vraiment figé ou perdu : l’espoir peut renaître, les structures se rouvrir, les habitudes se transformer. Il impulse du neuf là où tout semble figé.

Induction positive
Le Verseau fait le tri, élimine le pessimisme, les idées mortes, les pesanteurs inutiles. Il choisit d’oublier ce qui freine, pour se concentrer sur ce qui germe, ce qui promet, ce qui inspire. Il s’immunise contre le désenchantement en tournant résolument son regard vers l’avenir. Il croit aux lendemains meilleurs et met son énergie au service de cette foi lucide et constructive.

Lenteur d’inhibition
Sous son air toujours disponible, le Verseau se protège derrière des défenses solides, presque infranchissables. Il est ouvert, mais sans naïveté. Il sait se préserver du chaos ambiant afin de mieux nourrir son optimisme. Stoïque, tenace, impassible en apparence, il agit avec constance et rigueur, convaincu que les nouvelles voies qu’il perçoit doivent être patiemment construites, à l’abri des caprices du moment.

Sens des dosages
Le Verseau excelle dans l’art de l’équilibre subtil : il allie imagination et rigueur, lucidité et espoir, individualisme et solidarité. Il ne cherche pas à tout unifier dans une grande vision abstraite : il préfère jongler avec les contraires, doser, combiner, hybrider. Il défend la liberté tout en servant des causes universelles. Il veut changer le monde, mais sans imposer ; guider, mais sans contraindre.

Verseau - expression inadaptée
Faiblesse d’inhibition naturelle
Le Verseau mal intégré s’agite dans tous les sens sans jamais trouver de point d’ancrage. Il vit dans une frénésie continue, incapable de ralentir, de se poser, de se recharger. Il s’épuise, se disperse, ignore les besoins élémentaires de stabilité, de repos ou de stratégie. Il vit dans l’instant, sans prévoyance ni économie, et s’épuise à force de papillonnage. Un perpétuel courant d’air.

Vitesse d’excitation inadaptée
Tout le stimule trop vite, trop fort. Il réagit au quart de tour, change d’avis, passe du coq à l’âne, s’enflamme pour un rien. Son humeur est en dents de scie, il improvise sans filtre, s’emballe, puis retombe. L’inconstance règne : velléités avortées, euphorie sans cause, comportements erratiques. Il enchaîne les idées fulgurantes qui, faute d’enracinement, s’évanouissent aussitôt.

Phase paradoxale
Il se laisse éblouir par l’illusion du positif, au point de nier le réel. Une simple étincelle suffit à nourrir en lui des rêves démesurés, des espoirs irréalistes, des visions magiques. Il enjolive, promet, séduit par des projets extravagants, parfois manipulant les autres avec des mots brillants mais creux. L’enthousiasme devient poudre aux yeux, et l’utopie se transforme en mirage. Derrière les slogans, il ne reste souvent que du vent.""",

        "Pisces": """Poissons - expression adaptée
Force d’inhibition extinctive
À l’approche du Bélier et de la montée de l’élan diurne, le Poissons oppose une indifférence radicale : rien ne doit le troubler. Il se détache des pressions extérieures, se libère des conditionnements, se déprogramme des automatismes affectifs ou mentaux. C’est en se retirant du monde qu’il se rend disponible à l’essentiel. Son apparente capacité à tout accepter dissimule en réalité une distance absolue, une volonté de se rendre imperméable à toute influence.

Lenteur d’inhibition
Ses défenses sont stables, solides, inaltérables. Rien ne le bouscule : il oppose aux turbulences extérieures un calme implacable. Pas de réaction impulsive, mais un silence lourd de sens. Il laisse s’écouler le temps, décante les situations avec une patience tranquille. Cette impassibilité lui permet de rester à l’écoute de son intuition, sans se laisser distraire par l’agitation ambiante.

Sens des contraires
Plutôt que de savoir ce qu’il veut, il sait parfaitement ce qu’il ne veut pas. Il laisse venir, temporise, évite de trancher trop vite entre des choix opposés. Il avance entre les lignes, refuse les conflits frontaux, préfère se glisser entre les dualités sans jamais se figer dans l’un ou l’autre camp. Il use ses contradicteurs par le silence ou l’évitement. Pour lui, les oppositions perdent peu à peu de leur sens : il aspire à dépasser les antagonismes en recherchant une "troisième voie", plus englobante, plus profonde.

Poissons - expression inadaptée
Faiblesse d’excitation
Quand il ne parvient pas à affirmer sa volonté, le Poissons devient amorphe. Il flotte, s’efface, se résigne. Trop de mollesse, pas assez de combativité : la moindre difficulté l’abat. Il se laisse porter par les événements, subit sans agir. Il peut se replier dans un monde clos, en retrait du réel, prisonnier d’une passivité déprimante et d’un profond sentiment d’impuissance. Il fuit la confrontation, l’effort, la responsabilité.

Vitesse d’excitation inadaptée
Plus proche du Bélier, le Poissons mal équilibré peut connaître des débordements violents. Sous une surface calme couve une nervosité explosive. Il passe sans transition de l’apathie à la fureur : colères soudaines, agressivité imprévisible, pulsions incontrôlées. Il agit sans réfléchir, poussé par des vagues émotionnelles qu’il ne maîtrise pas, avant de retomber dans l’abattement ou la confusion.

Phase égalitaire
Tout devient flou, équivalent, sans relief : le monde perd ses contrastes. Plus rien ne touche, tout se vaut, tout se dissout. Cela peut évoquer une paix mystique… ou un vide total. Ne rien choisir, ne rien décider, attendre que le temps fasse ou défasse les choses. On se perd dans l’indistinction, dans l’idée que toute voie se vaut, que toute action est vaine. Cela peut conduire à une dilution de soi, jusqu’au renoncement à exister pleinement.""",
    },

    "EN": {
        "Aries": """Aries – Adapted Expression
Natural Excitation Strength
In the stage of Natural Excitation Strength, diurnal energy takes precedence over nocturnal inertia, sweeping away inhibitions and indifference. The energy is intact, raw, and ready to launch itself into the environment without restraint. This is primal aggressiveness, a pioneering impulse, a visceral craving for tangible, searing sensations. Spontaneity reigns, free from preconceptions: an instinctive, bold, and direct force that expresses itself generously. There is an imperative to act immediately, one that tolerates neither delay nor limitation.

Excitation Speed
Excitation Speed is characterized by the instantaneous mobilization of available energy: everything starts in a flash, reactions are immediate, decisions erupt spontaneously. One reacts on the spot, with sharp reflexes and a nearly automatic readiness to move. The pace is relentless, with endless self-acceleration. This high-strung dynamic often goes hand in hand with a cyclothymic temperament and a heightened adaptability to environmental shifts. Rapid excitation reveals a taste for dramatic effects: fanfares, vivid colors, impactful and striking visuals.

Sense of Contrasts
In this configuration of the Sense of Opposites, dominated by intense and rapid excitation, decisions are made without hesitation or nuance: one picks a side and sticks to it, often to the point of manichaeism. It’s all about brutal frankness and a rejection of compromise—the inner motto being: “You’re either with me or against me.” Choices are impulsive, instinctive—but when adaptation demands it, these decisions can be reversed just as violently as they were made. Radical 180-degree shifts are common, with the same fervor now fighting what was once passionately embraced.

Aries – Maladapted Expression
Inhibition Weakness
Unable to cultivate indifference, remain impassive, or take emotional distance, the impulsive type is swept up by the moment. Forgetting, detaching, starting fresh—none of this comes easily. He charges ahead no matter the consequences, intoxicated by the here and now. Reckless, impatient, and hasty, he acts without foresight or calculation. The inability to forget gives first impressions an indelible weight. This lack of distance—and thus, of reflection—leads to naïveté and credulousness: he is ready to believe almost anything.

Misadapted Inhibition Slowness
When the braking system malfunctions, two scenarios may occur. On one hand, there's the inability to brake at all: impulsivity runs wild, creating a perpetual clash with the external world, a string of accidents and excesses. On the other hand, once the brakes are applied, they can’t be released: the individual becomes stuck, locked into rigid, unilateral defense mechanisms. Refusals become absolute, grudges long-lasting, sometimes even pathological. The imagination becomes enthralled by legends and baroque myths, often drifting far from reality.

Egalitarian Phase
Here, aggressiveness takes on a linear, undifferentiated form, leading to a wholesale rejection of everything. No hierarchy, no discernment: everything is thrown into the same pile. Hostility becomes generalized and indiscriminate—“six of one, half a dozen of the other,” all are condemned alike. This blanket refusal affects friends and foes alike, denying the validity of both good and evil. Dialogue becomes impossible; thought locks into a rigid personal philosophy, impervious to challenge. The perception of opposites is abstracted into a “me versus the whole world” mindset, with no way out.""",

        "Taurus": """Taurus – Adapted Expression
Inhibition Strength
Taurus slows down, grows cautious, and settles. It moderates its vital energy, learns to regulate and conserve it. Its power follows a measured rhythm aimed at recovery and stability. There is an instinctive resistance to excess, waste, and haste. This voluntary retreat fosters mental and physical balance. Taurus knows how to pace itself, opposing the world’s turmoil with calm and steady inertia.

Negative Induction
Excitatory force narrows its focus onto a single object, where all energy and effort are concentrated. Nothing else matters: obsessive focus, intensive labor, relentless depth. Taurus devotes itself entirely to one field, one subject, one passion—sometimes to the point of extreme specialization or monomania. No distraction can divert it from its chosen path: willpower becomes unwavering fidelity to the object of investment.

Excitation Speed
Quick and reactive—but only when stirred by the object of Induction. Otherwise, Taurus remains calm, grounded, and unshaken. If external stimuli become overwhelming, adaptation requires a concrete anchoring in reality to avoid being overrun. Should this adaptation fail, Taurus may retreat into abstract or imagined worlds. When inhibition gives way under pressure, its apparent stillness can erupt violently—just one drop too many, and everything spills over. At a moderate balance, it alternates between calm and intensity, enjoying life's pleasures without excess: a lucid hedonist with a zest for living.

Sense of Dosage
The sense of moderation replaces the sharp dichotomy of opposites. It’s about finding balance between instinctive rejection and the compromises required by reality. Adaptation plays out in form without sacrificing substance. Taurus negotiates shrewdly without ever losing sight of practical self-interest. It may open to others, but always through the lens of prudence. In the face of adversity, it favors strategy over confrontation. Compromises are not an end in themselves—they serve to secure long-term dominance and control.

Taurus – Maladapted Expression
Excitation Weakness
Nothing surprises Taurus anymore. It expects no change, sees no novelty. Already weary, lazy, and dulled, it resists transformation, feels no thrill in discovery. It clings to past experiences, entrenched beliefs, rigid judgments. No more dreaming, no more imagining, no more hope: everything is fixed, static, condemned to repeat itself. Life slips into routine, and Taurus does the bare minimum to get by.

Misadapted Inhibition Slowness
It shuts itself off completely. Inhibitory inertia only deepens the lack of excitation: the brakes remain permanently engaged. Nothing pushes it to emerge from itself. A radical individualist, socially withdrawn, it retreats into rigid isolation. Over time, it hardens—becoming austere, doctrinaire, inflexible. Distrust becomes its default setting; communication breaks down; will turns to stubborn refusal. Its intuition strays far from contemporary norms, giving rise to hermetic, often schizoid mental constructions. A fortress of reinforced concrete takes shape around it.

Paradoxical Phase
Having lost the sense of intensities, Taurus overreacts to trivial signals. It reads hidden meanings into what’s clearly written, obsesses over minutiae, and invests disproportionate energy in insignificant matters. The tiny, the marginal, the invisible—these take on outsized importance. For those with strong potential, this might lead to surprising discoveries. For others, it results in chronic hypersensitivity or outright paranoia. All energy is funneled into the object of Induction—everything else is ignored. One becomes exhausted by a fixed idea, while the rest of the world fades into indifference.""",

        "Gemini": """Gemini – Adapted Expression
Excitation Strength
In Gemini, the Excitation Strength gains in finesse. The energy spreads out lightly, fluidly, and openly. The mind flutters with curiosity, eager to explore the endless facets of the world. A multitude of interests, a sharp curiosity, a taste for novelty, appearances, abstraction, and the play of ideas. There’s a vast inner openness: everything intrigues, attracts, or deserves a closer look. Adaptation occurs through the diversity of experience and the richness of perspectives.

Excitation Speed
At its peak. Reactions are swift, immediate, and flexible. Gemini shifts mentally and physically with ease, adapting effortlessly to change, surprise, or motion. It hops from one object to another, multiplies contacts, seizes fleeting opportunities. Versatile, light-hearted, and playful, it excels in quick transitions, unexpected associations, and sudden shifts of tone. This is a nimble, subtle, and inventive mind—always ready to pivot and play.

Sense of Wholeness
With inhibition pushed aside, there’s nothing to prevent the meeting of opposites. Gemini naturally lets the most heterogeneous elements interact, overlap, or combine. It intuitively perceives the larger dynamics that bind the most disjointed fragments. Everything is connection, everything is dialogue. It brings differences into contact without needing to dissolve them: universality arises from the respectful interplay of singularities. An instinctive humanist, a fluid mediator, Gemini fosters collective intelligence through flexibility, humor, and nuance.

Gemini – Maladapted Expression
Extinctive Inhibition Weakness
No filter, no restraint. Energy scatters without center or direction. Gemini becomes flighty, superficial, and so light it loses substance altogether. It skims everything, unable to focus, go deep, or commit. Highly suggestible, it is shaped by stronger wills, a naïve puppet of the moment. Reactions are impulsive, unconsidered, driven by whim. A mental draft, blown by passing winds.

Misadapted Inhibition Slowness
Two extremes emerge. Either inhibition is absent, and Gemini becomes a complete weather vane—nervous, erratic, and overwhelmed by mental agitation. Instability reigns, with no capacity for consistency. Or inhibition is locked tight, and intelligence retreats into an abstract, disembodied world. Gemini withdraws to a cold, theoretical ivory tower—or into nihilistic indifference, a disenchantment with life. In either case, the connection to reality is severed.

Ultraparadoxical Phase
The system inverts: what should inhibit now excites, and what should deter becomes enticing. Gemini plays with taboos, flirts with danger, delights in the absurd and paradoxical. It doubles itself, mimics, parodies, wears unexpected masks. Identity becomes fluid, blurred, permeable. It steps into the other’s shoes so completely, it risks losing itself. When its mental agility remains under control, it becomes a virtuoso of mediation, able to unite the seemingly irreconcilable. But without solid grounding, it falls into a permanent split—leaping between contradictions, escaping into illusion, twisting reason to justify the unjustifiable.""",

        "Cancer": """Cancer – Adapted Expression
Inhibition Strength
The Cancer instinctively establishes protective boundaries, shielding itself from overwhelming external stimuli. Within this enclosed space, it consolidates its strength, surveys its inner riches—emotional, intellectual, or otherwise—and reinforces the walls of its safe haven. This is the domain of self-containment, where one defends a cherished territory, a community, a personal sanctuary. It is also where one confronts oneself—wrestling with issues of self-worth, identity, and emotional subjectivity.

Excitation Slowness
Action unfolds slowly, patiently, with quiet persistence. The Cancer builds step by step, carefully and methodically. It opens to the outside world only with deliberation, ensuring that every movement is purposeful and contained. There’s a strong sense of inner discipline, a focus on stability and long-term structure. Rituals, habits, and routines create a solid framework that gives meaning to thoughts, feelings, and actions. Memories, traditions, and internal safeguards shape a consistent and enduring worldview.

Sense of Wholeness
Here, the diurnal energy still reigns, but it wanes—it no longer seeks to receive, but to integrate. Cancer embodies the synthesis of an inner world enclosed within limits: it is the place of greatest content. All is gathered under one roof, within one framework, preserving a total memory and living out every nuance of one's inner universe. It is a cohesive world, defended from intrusion, governed by an enduring will to maintain continuity and coherence. This is the strength of inner wholeness, loyalty, and homogeneity.

Cancer – Maladapted Expression
Associative Excitation Weakness
There’s a refusal—or an inability—to connect with others or the outside world. Cancer withdraws into its shell, cutting ties, avoiding contact, and isolating itself from any external input. It settles into inertia, gives in to lethargy, becomes passive, nostalgic, or apathetic. Uncommunicative and inward-looking, it clings to its comforts and rejects perspectives that challenge its own. Its inner world becomes a closed circuit, recycling the same emotions and thoughts in a loop of self-absorption.

Misadapted Inhibition Speed
Reactions of inhibition come too fast, too strong, or in the wrong context. Cancer retreats at the first sign of imagined danger, misreads situations, and overreacts defensively. There is avoidance, fear, anxiety for no clear reason. The external world is perceived as hostile by default. Decisions are paralyzed by doubt, discrimination misfires, and worry becomes obsessive. Everything unfamiliar is met with suspicion or panic—an intrusion into the sanctum must be repelled, regardless of its intent.

Ultraparadoxical Phase
Boundaries blur and opposites blend: inside and outside lose their meaning. The homebody dreams of far-off adventures, the wanderer longs for a hearth. The real and the imaginary intertwine, subjectivity spills into objectivity, and one becomes entangled in emotional or mental feedback loops. Emotions are felt about emotions, thoughts spiral around themselves. All piles up in a closed space: a clutter of dreams, fears, impressions—fragmented, unrelated, directionless. Protection becomes fixation: family, place, or authority become absolute anchors, while gestures of openness or cooperation trigger anxiety or flight.""",

        "Leo": """Leo – Adapted Expression
Releasing Excitation Strength
Leo instinctively resists all forms of limitation, confinement, or stagnation. It responds with power and courage to anything that restricts its movement or ambition. The impulse is to break free, to rise above, to shatter constraints — to triumph over adversity and assert one's autonomy. Leo dares, leads, expands, radiates. It strives not only to overcome obstacles, but to affirm itself as a sovereign force, heroically and proudly stepping into its full potential.

Positive Induction
By concentrating protective inhibition on a select core, Leo creates a fortified inner sanctuary. This enables it to act boldly, generously, and confidently from a position of inner security. The ego is centered but expansive — an open-hearted self-assurance. This is the realm of magnanimity, leadership, and authentic charisma: the ability to shine brightly without fear of being dimmed.

Excitation Slowness
Leo’s actions are deliberate and calculated. It values structure, control, and lasting impact. Goals are pursued with unwavering persistence, and passions, though intense, are sustained over time. Risks are taken, but never recklessly — they are part of a long-term vision. The Leo temperament thrives on mastery: of self, of purpose, of destiny. Its authority is not only earned, but carefully maintained.

Sense of Dosage
Leo transitions from a sense of totality to a refined sense of proportion. It must balance personal ambition with collective demands; assert power without suffocating others. It knows how to negotiate, to appear generous while securing influence. This is the strategy of the “long leash” — granting apparent freedom to others while ultimately keeping control. When well-managed, this ambivalence allows Leo to lead with authority and grace, combining directive strength with liberal tolerance.

Leo – Maladapted Expression
Differential Inhibition Weakness
Subtlety vanishes. The maladapted Leo is clumsy, overbearing, and socially tone-deaf. There’s no finesse, no tact, no nuance — just brute force and unfiltered expression. It barges in, dominates conversations, and makes a spectacle of itself. Without the capacity for refined discrimination, it lacks the strategic hypocrisy often necessary in human relations. What remains is bombastic, simplistic bravado: the social equivalent of a bull in a china shop.

Misadapted Inhibition Speed
Beneath the bravado lies a deep fear: the fear of losing face, control, or prestige. Leo may act bold, but sudden anxiety about its vulnerability can paralyze or derail its efforts. It may bluff to hide fear, or abandon bold plans in a wave of panic. Facing real threats, it may retreat dramatically to avoid humiliation — unless it charges forward blindly in a desperate attempt to preserve its image.

Paradoxical Phase
Strikingly, the Leo paradox is this: true danger barely fazes it, but a minor bruise to the ego can unleash dramatic overreaction. Tickle its pride, and you may trigger a storm. Mention a global crisis, and it might remain unmoved. This inverted sensitivity leads to misplaced priorities: it glorifies spectacle and grandeur while dismissing nuance and substance. Overconfident in reckless ventures, it underestimates real risks. By craving victory too visibly, Leo opens the door for more cunning players to outmaneuver it.""",

        "Virgo": """Virgo – Adapted Expression
Blocking Inhibition Strength
In Virgo, the brakes are firmly engaged: protection is close-range, methodical, and tightly controlled, ensuring maximum efficiency. One renounces the unattainable, builds safety margins, and keeps backup plans in place. There is a drive to limit oneself, to be self-sufficient, to avoid being overwhelmed or corrupted by anyone or anything. Every necessary precaution is taken to secure independence and shield from need or dependence.

Excitation Slowness
Action unfolds slowly but surely — methodical, hierarchical, and meticulously planned. Beneath an appearance of restraint lies an invisible yet relentless determination, yielding reliable outcomes with minimal waste. Rigor, seriousness, method, and patience are elevated to ideal virtues. Without fanfare, the goal remains clear. Habits become near-sacred rituals. Space is compartmentalized and domesticated for full control.

Sense of Contrasts
Thanks to the blocking inhibitory force, boundaries between self and others are sharply defined. Mixing is avoided; there’s an acute awareness of concrete incompatibilities and immutable oppositions. Clear lines are drawn between self and world, right and wrong, permitted and forbidden — all coexisting without blending. This manifests as a tendency toward classification, purism, or selective segregation. To preserve inner integrity, one may even deliberately wear a mask contrary to their true nature.

Virgo – Maladapted Expression
Associative Excitation Weakness
In maladaptive Virgo, associative excitation is nearly absent: no drive, no spontaneity, no willingness to connect, share, or synchronize thoughts, actions, or emotions with others. The individual turns entirely inward, withdrawing into a narrow inner world and a fragmented self. Self-protection becomes almost masochistic, forbidding any form of freedom, daring, or aspiration. This may give rise to deep-seated feelings of inferiority. Emotional exchanges are absent; there's impenetrability, a refusal to engage, or even negotiate.

Misadapted Inhibition Speed
Defensive mechanisms operate as if detached from reality: there is a constant fear of intrusion, a never-ending anxiety, like an ostrich too afraid to lift its head from the sand. Every pretext becomes a reason to withdraw: fear of germs, law enforcement, theft, confrontation, others — even oneself. This can spiral into anxiety neurosis or neurasthenia. Yet, the speed of inhibition hovers at the edge of adaptability: fear may conceal discreet desires, or suppressed courage may emerge through irony, distant sarcasm, or veiled criticism.

Egalitarian Phase – Clash of Contrasts
Why “clash of opposites”? Because as day and night approach equal duration, the maladaptive Virgo becomes acutely sensitive to extreme contrasts. These are experienced as painful internal dilemmas — paralyzing conflicts between desire and duty, self and other, lawful and unlawful. The equalizing phase amplifies this anxiety: the Virgo native becomes chronically distrustful, regardless of how others behave. Depending on temperament, this may lead either to psychasthenic withdrawal or, more actively, to intolerance, allergic reactivity toward others, and sectarianism — an inability to truly mix with anyone, not even one’s closest allies.""",

        "Libra": """Libra – Adapted Expression
Associative Excitation Strength
As the diurnal world of summer comes to an end, Libra ushers in the nocturnal phase: one turns away from the self to open up to others, to engage with the external world on equal footing. It is a time for connection, exchange, dialogue, and harmonious coexistence with an environment seen as a partner. The Libra mindset seeks to link, reconcile, and smooth over differences. One reaches out with diplomacy and a spirit of compromise, moving past opposition with grace.

Inhibition Speed
Defensive reactions are swift, flexible, and appropriate: fear does not paralyze, it is contained and skillfully redirected. Libra learns to move with finesse through social interactions, to avoid direct clashes, and to employ social codes—politeness, elegance, rhetorical finesse—to defuse tension. Thought processes rely on subtle distinctions and refined analysis. The ability to recognize opposing forces enables thoughtful arbitration and a continual pursuit of balance and harmony.

Sense of Contrasts
Libra does not make sharp, unilateral choices: it brings opposites together, compares them, weighs their interactions, and strives to make informed, inclusive decisions. Every option is viewed as the complement of another, not its adversary. This outlook may lead to hesitation or inner dilemmas, but also to a uniquely rich intellectual depth. The desire for fairness and the fear of excluding or making the wrong choice inspire careful, sophisticated reflection.

Libra – Maladapted Expression
Blocking Inhibition Weakness
All frameworks, boundaries, and constraints are rejected: the maladapted Libra falls into a naïve universalism, rushing headlong into all experiences without discernment. It is total laissez-faire, a reckless openness to danger, a “derangement of all the senses” (Rimbaud). Freedom without structure turns into licentiousness. With no self-discipline, no guiding norms, and no enduring foundations, nothing is defended or built. Commitment is constantly evaded.

Misadapted Excitation Slowness
The need for order, control, and organization is misdirected or misplaced: effort is poured into imaginary constructs, grand illusions, and fantasies of personal omnipotence. Reality dissolves into castles in the air, meaningless causes, or futile battles against imagined enemies. There is a retreat into vague romanticism, mystical dreams of limitless power, or the self-congratulatory pride of never taking a stand.

Egalitarian Phase
Everything is seen as equal, and nothing is distinguished: the maladapted Libra refuses to choose, eager to please everyone, circulating through all circles without ever taking a clear position. This relentless openness slides into compromise. All edges are smoothed, even when a firm stance is needed. Indecision turns into indifference, and the constant drive to reconcile degenerates into opportunism. The self becomes a mirror of its era or environment, prioritizing popularity over authenticity.""",

        "Scorpio": """Scorpio – Adapted Expression
Differential Inhibition Strength
Scorpio perceives first and foremost what separates, distinguishes, and divides: it dissects, analyzes, discriminates, and tracks down the slightest nuances. Wary of overly simplistic associations, it prefers to emphasize contrast: seeking flaws, stoking tensions, deepening divisions, asserting its singularity. This sharp sense of discernment leads Scorpio to explore zones of rupture with clarity and precision.

Negative Induction
Its associative excitement is narrow, exclusive, almost fusion-like. Scorpio favors intense, closed alliances, deep commitments, unbreakable vows. Its perception zeroes in on fine details, contractual loopholes, and the subtleties of relationships. Each moment is lived with a heightened sense of significance, as if charged with crucial or historical meaning.

Inhibition Speed
Scorpio is an ultra-reactive inhibited type, a master of intelligent evasion. Cunning and agile, it slips skillfully through traps and perilous situations. Its mind is razor-sharp, instantly grasping the hidden workings behind appearances. Scorpio deftly handles veiled threats and ambiguous promises, maintaining firm convictions while adapting its style with remarkable flexibility.

Sense of Dosage
In its adaptive mode, Scorpio balances a taste for contrast with a desire for coherence. It knows how to unite opposites within a single vision. It plays with tension to integrate it, using double games strategically without losing sight of its deeper aim. Negotiating with adversaries — to better understand or subdue them — making pacts without betrayal: Scorpio thrives on the fault lines, where relational intensity and strategic control converge.

Scorpio – Maladapted Expression
Blocked Excitation Weakness
Withdrawn into itself, trapped within its own singularity, the maladaptive Scorpio becomes unable to transcend or open up. It sinks into a closed, dark, stagnant world: emotional morass, suffocating environments, a sense of fatal destiny. Clinging to its pain, failures, and flaws, it ends up embracing them as proof of fidelity to itself — even if it means perpetuating suffering. It spirals in the prison of a wounded identity.

Misadapted Excitation Slowness
Obsessed with its internal representations, it develops a pathological need for control in closed environments. Believing itself endowed with secret, unique, almost magical powers, it draws strength from rigid fixity and intolerant subjectivity. Its opposition becomes sterile and prideful. It operates from the shadows, manipulating and exploiting others without remorse, thriving on their suffering in a cold, calculating drive for domination.

Paradoxical Phase
Losing its sense of proportion, Scorpio overreacts to weak signals. Its hyper-discriminating mind fixates on the hidden, the taboo, or the marginal — whether real or imaginary. It fosters mystery, veiled threats, and ominous insinuations. Fascinated by the dark and the obscure, it turns to manipulation: blackmail, cryptic warnings, twisted strategies. It dramatizes excessively, paints everything black, becoming a harbinger of doom. In extreme cases, it seeks to control everything, pulling strings from behind the scenes through relentless maneuvering and Machiavellian schemes.""",

        "Sagittarius": """Sagittarius – Adapted Expression
Associative Excitation Strength
Sagittarius shines in the art of connection. It links, correlates, and weaves together the most distant and diverse domains. It sees bridges where others see walls. Deeply sensitive to large-scale interactions, it embraces a global — even cosmic — understanding of the world. The self dissolves into the collective: one becomes a link in a vast chain of meaning and cooperation. Open, generous, and outgoing, Sagittarius is ready to go above and beyond to serve universal ideals, often sacrificing the personal in favor of the collective.

Inhibition Speed
Sagittarius masters the subtle art of graceful avoidance. With social finesse and instinctive diplomacy, it knows when to step in and when to step away. It moves effortlessly through cultural codes, advocating for openness while maintaining the ability to filter and select. Though it dreams of endless connections, in practice it’s selective — an enlightened elitism guides its choices. It promotes inclusiveness but not at the cost of discernment.

Sense of Wholeness
The Sagittarian spirit is in search of an infinite macro-synthesis where everything fits, everything connects — smoothly and dynamically. From the micro to the macro, the material to the celestial, it sees a unified, interdependent cosmos. This is not “we need everything to make a world,” but rather “the world is one harmonious whole.” Its vision transcends dualities and divisions, striving to integrate all aspects of the self and world into a fluid, coherent unity. It thrives on hybridization, fusion, and a deep-rooted desire to reconcile opposites within a broader, harmonious framework.

Sagittarius – Maladapted Expression
Blocking Inhibition Weakness
The maladaptive Sagittarius rejects all constraint and limitation. Rules, norms, and boundaries are intolerable. It becomes impulsive, reckless, impatient — ready for any excess or extreme. It chases the unreachable, flees toward abstraction, the infinite, the unattainable. There’s no instinct for self-preservation. It breaks out of one prison only to get lost in a fantasy of freedom. Limits feel like insults, and realism is dismissed in favor of grand, illusory quests.

Misadapted Excitation Slowness
The urge to organize or control focuses on the colossal. It must be big, magnificent, larger-than-life. Imagination spirals into mythomania — delusions of grandeur, megalomania, heroic fantasies. There’s a relentless drive for power or transcendence, often masking a hollow, shapeless personality. It identifies with mythical figures or indulges in pompous seriousness to conceal its lack of grounding. It dreams of glory but fails to establish the realistic foundations necessary for success.

Ultraparadoxical Phase
The Sagittarian paradox goes off the rails when it tries to reconcile the irreconcilable. It seeks harmony between radically opposed views, falling into chaotic syncretism and incoherent mixes. What should inhibit instead stimulates: it is drawn to risk, danger, and absurd bets. It burns through its reserves with enthusiasm. At once hyper-social and claiming originality, it becomes the revolutionary of the drawing room, the conformist in anti-conformist clothing. By endlessly minimizing threats and thinking even wolves can be tamed with politeness, it ends up sabotaging itself, giving power to adversaries in the name of idealistic openness.""",

        "Capricorn": """Capricorn – Adapted Expression
Extinctive Inhibition Strength
Capricorn dwells in an inner world, focused solely on what truly matters. He instinctively filters out the trivial and distances himself from superficial stimuli. Cold, detached, at times even glacial, he remains unmoved by daily disturbances. This isn’t indifference — it’s unwavering commitment to the essential. He knows how to let go, how to forget, how to disengage from the noise of the world in order to remain loyal to his core values. Detachment is his strength, and stillness his power.

Inhibition Slowness
His reactions are slow, but deeply rooted. He builds for the long term, with persistence and unshakable determination. Protected by strict principles and inner discipline, he is nearly immune to external fluctuations. Nothing shakes him easily. He relies on rigor, patience, strategy, and a taste for simplicity and structure. He is methodical and steady, guided by an intuitive grasp of invisible frameworks and underlying systems.

Sense of Wholeness
Capricorn seeks to understand the foundations of things — the deep laws, the hidden architectures of reality. He strives for a world where everything is in its place, organized with precision and cohesion. He doesn’t just connect ideas or people — he structures them. He wants each piece to fit perfectly, each person to play their role in a larger, harmonious whole. His is an abstract form of humanism: if each individual functions as a well-adjusted cog in the larger system, all will go well. Integrity, discipline, and respect for necessary order guide his every move.

Capricorn – Maladapted Expression
Natural Excitation Weakness
In his maladapted form, Capricorn loses all spontaneity. There’s no vitality, no initiative, no drive. He fades into passivity, into self-erasure. He doubts his worth, feels powerless, unable to respond to the world’s demands. Everything seems like a burden. He withdraws into a dull inertia, devoid of emotion or desire. He becomes expressionless, unreachable, emotionally shut down — locked in a state of deep fatigue and disinterest.

Misadapted Excitation Speed
He struggles to get moving. Sometimes, he freezes completely, gripped by a hidden restlessness that he cannot or will not express. Other times, he stirs into erratic motion — brief bursts of unfocused energy, minor outbursts, fickle moods — only to collapse again into numbness. He swings between rigid immobility and pointless agitation, unable to find balance or direction.

Ultraparadoxical Phase
What should excite him instead shuts him down. Openness, novelty, and uncertainty trigger rejection. Even good news leaves him cold. He clings stubbornly to old habits, even when the situation clearly calls for a strong response. He may crave what he despises, or disdain what he secretly desires. In extreme cases, he becomes entirely consumed by a higher Cause — the Law, Morality, Duty, or some Sacred Principle. He sacrifices himself to this ideal, to the point of forgetting his own needs and feelings. Cold fanaticism, icy devotion: he becomes the merciless executor of a mission no one asked of him, ready to give everything — even what should be left untouched — in service of a transcendent absolute.""",

        "Aquarius": """Aquarius – Adapted Expression
Regenerative Excitation Strength
Aquarius refuses to sink into apathy or despair. When faced with disillusionment or rigidity, they respond with a powerful drive for renewal. They shed old skins, transform perspectives, breathe new life into stagnant ideas. For them, nothing is ever truly lost—everything can be reborn. They challenge conventions, refresh routines, and open closed systems with a liberating optimism.

Positive Induction
Their focus is selective: they deliberately ignore what drags them down—pessimism, cynicism, and worn-out values are left behind. Aquarius immunizes themselves against despair by tuning in to what’s growing, evolving, and promising. They’re drawn to budding potential, future breakthroughs, and optimistic visions, channeling their energy into creating better tomorrows.

Inhibition Slowness
Despite their outward openness, Aquarius maintains deep, solid defenses. They’re hopeful, but not reckless. They protect their ideals from outside chaos through stoic detachment and inner discipline. Their calm in the face of adversity is not passivity, but a strategic choice to maintain their long-term vision. Their drive to spark progress comes with a core of unshakable perseverance.

Sense of Dosage
Aquarius excels at balancing opposites: idealism with pragmatism, individuality with collective causes, vision with precision. They move from abstract unity to concrete balance—mixing originality and discipline in unique proportions. They seek to lead through values, not ego, and to support others’ freedom while advancing their own ideals. They embody a thoughtful, tempered revolution.

Aquarius – Maladapted Expression
Natural Inhibition Weakness
When off balance, Aquarius never slows down. They burn themselves out in restless hyperactivity, unable to rest, recover, or settle. With no grounding, no stable base, they live on the surface of life, ignoring practical needs and draining their energy. Like the fable’s grasshopper, they dance through life with no roots or long-term plan—chaotic, scattered, unsustainable.

Misadapted Excitation Speed
With weak inhibition, their reactions become erratic and impulsive. Moods swing wildly, thoughts leap from one topic to another. They get hyped over nothing, act out of turn, improvise without aim. Sudden highs are followed by empty lows. Enthusiastic bursts fade as quickly as they appear, leaving behind only confusion and fatigue. Their energy becomes a whirlwind of incoherence.

Paradoxical Phase
They overvalue promise and potential, ignoring warning signs or uncomfortable truths. Even the smallest glimmer of hope can spark wild dreams or utopian visions. Optimism becomes reckless, imagination detaches from reality. They may try to dominate through charisma, grand illusions, or messianic claims—offering miracle solutions or dazzling promises that amount to smoke and mirrors. The show dazzles, but there’s little substance behind the shine.""",

        "Pisces": """Pisces – Adapted Expression
Extinctive Inhibition Strength
As the daytime world begins to rise—soon to dominate in Aries—Pisces holds fast in profound indifference. It refuses to be touched, shaken, or influenced by anything or anyone. Pisces detaches from external pressures, erases conditioning, clears the slate of habitual reactions, feelings, and thoughts. It withdraws from the surrounding world to be fully present to itself and to the absolute it seeks. What seems like total adaptability is, in truth, a complete emotional and mental distancing.

Inhibition Slowness
Its defensive systems are rigid, immovable, and serene. Pisces calmly resists outside turmoil. It decants slowly, responding to nothing impulsively. Its placid detachment from the world allows deep intuition to flow freely. The silence is not passivity, but a conscious refusal to engage prematurely, a waiting space for inner clarity to emerge.

Sense of Contrasts
Pisces may not know exactly what it wants, but it knows with precision what it doesn’t want. It delays choices between conflicting paths, letting tensions settle before deciding. It avoids clear-cut binaries, slips between polarities, refusing to be trapped in dualisms. It wears down opponents through non-reaction, dodging direct conflict. In a static inner world where opposites blur, Pisces seeks a "third way"—a transcendent synthesis beyond false dilemmas.

Pisces – Maladapted Expression
Natural Excitation Weakness
Pisces struggles to assert, act, or fight. It becomes sluggish, amorphous, passive to the point of paralysis. It drifts with circumstances, hoping for the best, but lacking drive. It avoids effort, resists reality, and may retreat into emotional or physical isolation. This leads to dependence, confinement, fatigue, inefficiency, and a suffocating inability to communicate or engage with the real world.

Misadapted Excitation Speed
Closer to Aries, Pisces can express bursts of emotional reactivity. Beneath its still surface lie stormy waters: suppressed passions erupt into sudden rages, blind anger, or erratic aggression. These outbursts are uncontrolled and often disproportionate, followed by a return to exhaustion or despondency. The mood swings between apathy and rebellious bitterness.

Egalitarian Phase
Everything seems equal, indistinguishable, without contrast. Nothing excites or disturbs. The world feels flat and unmoving. This can feel like spiritual serenity—or like nihilistic emptiness. Passive non-choosing leads to the loss of self: one becomes nothing in the whole, everything in nothing, and ultimately, nothing at all. Pisces waits, either for a resolution or for collapse, until all reasons for choosing—good or bad—are shattered by the clash of opposites.""",
    },
}
