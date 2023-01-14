
create table if not exists users (
    id integer primary key autoincrement,
    username text unique not null,
    password text not null
);

create table if not exists category (
    id integer primary key autoincrement,
    category_type text unique not null
);

create table if not exists challenge (
    id integer primary key autoincrement,
    category_id integer,
    file_id integer,
    descript text unique not null,
    foreign key(category_id) references category(id),
    foreign key(file_id) references instruction_movies(id)
);

create table if not exists movies (
    id integer primary key autoincrement,
    uploader integer,
    challenge_id integer,
    likes integer,
    foreign key(uploader) references users(id),
    foreign key(challenge_id) references challenge(id)
);

create table if not exists instruction_movies (
    id integer primary key autoincrement,
    file_name text unique not null
);

create table if not exists likes (
    id integer primary key autoincrement,
    user_id integer not null,
    file_id integer not null,
    foreign key(user_id) references users(id),
    foreign key(file_id) references movies(id)
);
INSERT OR IGNORE INTO users (username, password) VALUES ("a", "a");

INSERT OR IGNORE INTO category (category_type) VALUES ("tricks");
INSERT OR IGNORE INTO category (category_type) VALUES ("cooking");
INSERT OR IGNORE INTO category (category_type) VALUES ("sport");
INSERT OR IGNORE INTO category (category_type) VALUES ("education");

