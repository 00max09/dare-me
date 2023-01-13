
create table if not exists users (
    id integer primary key autoincrement,
    username text not null,
    password text not null
);

create table if not exists movies (
    id integer primary key autoincrement,
    moviename text not null,
    uploader text not null,
    category text not null,
    likes integer
);

create table if not exists challenge (
    id integer primary key autoincrement,
    category text not null,
    descript text not null
);
