-- 创建数据库
create database if not exists design_pattern;


-- 创建单机游戏表
-- mysql 中的 blob 最大 65535，该表中的img字段超过，大概74321，需要使用 longblob
-- 图片不推荐保存在数据库
create table if not exists single_game(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null unique,
	`game_type` varchar(255),
	`game_release` varchar(255),
	`game_release_date` date,
	`game_arrange_date` date,
	`game_platform` varchar(255),
	`game_website` varchar(255),
	`game_label` varchar(255),
	`game_language` varchar(255),
	`game_score` double(2, 1),			-- 精度，评分10可以吗？
	`game_rater_num` int(11),
	`game_img` varchar(255)				-- 存储图片
)




-- 创建安卓游戏表
create table if not exists android_game(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null unique,
	`game_slogan` varchar(255),
	`game_version` varchar(255),
	`game_platform` varchar(255),
	`game_type` varchar(255),
	`game_release_date` date,
	`game_release` varchar(255),
	`game_language` varchar(255),
	`game_score` double(2, 1),
	`game_rater_num` int(11),
	`game_img` varchar(255)
)



-- 创建苹果游戏表
create table if not exists ios_game(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null unique,
	`game_slogan` varchar(255),
	`game_version` varchar(255),
	`game_platform` varchar(255),
	`game_type` varchar(255),
	`game_release_date` date,
	`game_release` varchar(255),
	`game_language` varchar(255),
	`game_score` double(2, 1),
	`game_rater_num` int(11),
	`game_img` varchar(255)
)




-- 创建网页游戏表
create table if not exists online_game(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null unique,
	`game_hope_num` int(11),
	`game_type` varchar(255),
	`game_frame` varchar(255),
	`game_develop` varchar(255),
	`game_operator` varchar(255),
	`game_website` varchar(255),
	`game_status` varchar(255),
	`game_label` varchar(255),
	`game_score` double(2, 1),
	`game_rater_num` int(11),
	`game_img` varchar(255)
)