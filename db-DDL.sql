create table league
(
    league_id        varchar(40) not null
        primary key,
    league_country   varchar(80),
    sport   varchar(80),
    league_logo      varchar(70),
    league_name      varchar(35),
    league_name_i18n varchar(255)
);

alter table league
    owner to wohhu;

create table news
(
    news_id      varchar(40) not null
        primary key,
    news_content varchar(16392),
    image        varchar(255),
    published    timestamp(6),
    news_summary varchar(8196),
    news_tags    varchar(350),
    title        varchar(600)
);

alter table news
    owner to wohhu;

create table player
(
    player_id       varchar(40) not null
        primary key,
    player_country  varchar(40),
    player_dob      date,
    player_name     varchar(70),
    player_photo    varchar(128),
    player_position varchar(40)
);

alter table player
    owner to wohhu;

create table season
(
    season_id    varchar(40) not null
        primary key,
    season_name  varchar(35),
    season_end   date,
    season  _start date,
    league_id    varchar(40) not null
        constraint fks8kd4aueryljws3a8kj228jvm
            references
);

alter table season
    owner to wohhu;

create table sport
(
    sport_id   varchar(40) not null
        primary key,
    is_active  boolean,
    desc_i18n  varchar(1024),
    logo       varchar(128),
    sport_mode varchar(17)
        constraint sport_sport_mode_check
            check ((sport_mode)::text = ANY
                   ((ARRAY ['BOTH'::character varying,
                    'BY_TEAM'::character varying,
                    'INDIVIDUAL'::character varying])::text[])),
    name_i18n  varchar(255),
    point_name varchar(70)
);

alter table sport
    owner to wohhu;

create table stadium
(
    stadium_id varchar(255) not null
        primary key,
    capacity   integer,
    country    varchar(40),
    desc_i18n  varchar(1024),
    name       varchar(255),
    photo      varchar(255)
);

alter table stadium
    owner to wohhu;

create table tournament
(
    tournament_id   varchar(255) not null
        primary key,
    team_country    varchar(40),
    desc_i18n       varchar(1024),
    end_date        date,
    logo            varchar(128),
    name_i18n       varchar(255),
    season          varchar(40),
    start_date      date,
    tournament_year integer
);

alter table tournament
    owner to wohhu;

create table team
(
    team_id       varchar(40)  not null
        primary key,
    team_country  varchar(3),
    team_desc     varchar(255),
    team_logo     varchar(128),
    team_name     varchar(128),
    sport_id      varchar(40)  not null
        constraint fkk1sdogt0khby5wtn58a2j1rdn
            references sport
);

alter table team
    owner to wohhu;

create table league_team
(
    instance_id   varchar(40) not null
        primary key,
    team_meta     varchar(255),
    team_position integer,
    league_id     varchar(40) not null
        constraint fk42nqg93tcmnm42c9jjvl4nr4k
            references league,
    season_id     varchar(40) not null
        constraint fkjaeynp5h4dwswmu65ad73sqcy
            references season,
    team_id       varchar(40) not null
        constraint fkwwjm5nxr1jrlklf5l0aqum7k
            references team
);

alter table league_team
    owner to wohhu;

create table match
(
    match_id      varchar(255) not null
        primary key,
    match_country varchar(3),
    end_time      time(6),
    match_date    date,
    name          varchar(70),
    place         varchar(128),
    start_time    time(6),
    league_id     varchar(40)
        constraint fk524ycxnj02ukjb4gghuqh1rod
            references league_team,
    stadium_id    varchar(255)
        constraint fkojlcqppbrrr1l8kd4b8ta35sp
            references stadium

);

alter table match
    owner to wohhu;

create table match_detail
(
    match_detail_id varchar(255) not null
        primary key,
    home            boolean,
    visitor         boolean,
    match_id        varchar(255)
        constraint fkd9wrmrjlb1sydqo42dmpb1xxo
            references match,
    team_id         varchar(40)
        constraint fk5u2jk9e91vv1s31vidgjpnw2v
            references team
);

alter table match_detail
    owner to wohhu;

create table score_entity
(
    score_id        varchar(40)      not null
        primary key,
    points          double precision not null,
    match_detail_id varchar(255)
        constraint fk6dpior2ifpl309rmt20x2qowo
            references match_detail
);

alter table score_entity
    owner to wohhu;

create table team_players_entity
(
    player_meta varchar(255),
    season_id   varchar(40) not null
        constraint fkh0a065ra217hajcrw429cueq1
            references season,
    team_id     varchar(40) not null
        constraint fk91sdygsi6rxsivpcxjwfut803
            references team,
    player_id   varchar(40) not null
        constraint fkr42bm4vlwicexlqtxjxaexgs9
            references player,
    primary key (player_id, season_id, team_id)
);

alter table team_players_entity
    owner to wohhu;

