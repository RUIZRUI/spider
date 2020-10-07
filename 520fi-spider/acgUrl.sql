use spider;

create table if not exists `520_fi_acg` (
    `acg_id` int(11) auto_increment primary key,
    `acg_url` varchar(255) not null unique
);