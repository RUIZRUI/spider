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



-- 创建单机游戏排行榜表
create table if not exists single_game_rating(
	`game_id` int(11) primary key,
	`game_name` varchar(255) not null unique,
	`game_english_name` varchar(255) not null unique,
	`game_type` varchar(255),
	`game_develop` varchar(255),
	`game_platform` varchar(255),
	`game_release` varchar(255),
	`game_release_date` date,
	`game_language` varchar(255),
	`game_website` varchar(255),
	`game_label` varchar(255),
	`game_score` double(2, 1),
	`game_rater_num` int(11),
	`game_img` varchar(255) 
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


-- 创建安卓游戏排行榜表
create table if not exists android_game_rating(
	`game_id` int(11) primary key,
	`game_name` varchar(255) not null unique,
	`game_slogan` varchar(255),
	`game_size` varchar(255),
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


-- 创建苹果游戏排行榜表
create table if not exists ios_game_rating(
	`game_id` int(11) primary key,
	`game_name` varchar(255) not null unique,
	`game_slogan` varchar(255),
	`game_size` varchar(255),
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



-- 创建网页游戏排行榜表
create table if not exists online_game_rating(
	`game_id` int(11) primary key,
	`game_name` varchar(255) not null unique,
	`game_hope_num` int(11),
	`game_type` varchar(255),
	`game_frame` varchar(255),
	`game_test_date` date,
	`game_develop` varchar(255),
	`game_operator` varchar(255),
	`game_website` varchar(255),
	`game_status` varchar(255),
	`game_label` varchar(255),
	`game_score` double(2, 1),
	`game_rater_num` int(11),
	`game_img` varchar(255)
)



-- 评论表
-- table的存储引擎只能是InnoDB，因为只有这种存储模式才支持外键
-- 为了查询我的评论性能，数据库将继承关系保存为 user_id_from, user_id_to，查询复杂度由O(n^2)降到O(n)
-- foreign key(user_id_to) references comments(user_id_from) 必须错，因为user_id_from不唯一
create table if not exists comments(
	comment_id int(11) auto_increment,
	user_id_from int(11) not null,		-- 发送评论的用户
	user_id_to int(11),					-- 接收评论的用户，如果是游戏，则为null
	game_id varchar(255) not null,
	parent_id int(11),
	content text not null,
	comment_time timestamp default current_timestamp(),
	likes int(11) default 0,
	dislike int(11) default 0,
	primary key(comment_id),
	foreign key(user_id_from) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
	foreign key(parent_id) references comments(comment_id)
	ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
	foreign key(user_id_to) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE,		-- 外键约束
	index index_id(comment_id)
)engine=InnoDB;


-- 获取一个游戏的所有评论
-- 每一条评论包括: comment_id, user_id_from, parent_id, content, comment_time, img, user_name, priority
select c.comment_id, c.user_id_from, c.parent_id, c.content, c.comment_time, u.img, u.user_name, u.priority
from comments as c, user as u
where c.game_id = ? and c.user_id_from = u.user_id; 

-- 获取我发出的评论
-- 通过game_id获取游戏名
-- c.user_id_to is null时，comments表和user表连接后，没有连接条件，再distinct性能会很低
-- 第一种写法
select distinct c.comment_id, if(c.user_id_to is null, null, u.user_name), c.game_id, c.comment_time
from comments as c, user as u
where c.user_id_from = ? and (c.user_id_to is null or c.user_id_to = u.user_id)
-- 第二种写法
-- where条件中的 and c.user_id_from = u.user_id 仅仅是为了多表连接时限制数目，防止重复
select c.comment_id, if(c.user_id_to is null, null, u.user_name), bg.game_name, bg.game_belong, c.comment_time
from comments as c, user as u, base_game as bg
where c.user_id_from = ? and ((c.user_id_to is null and c.user_id_from = u.user_id) or c.user_id_to = u.user_id) and c.game_id = bg.game_id
-- 第三种写法
-- union all不去重复值，效率比 union高很多
select comment_id, null, game_id, comment_time
from comments
where user_id_from = ? and user_id_to is null
union all		
select c.comment_id, u.user_name, c.game_id, c.comment_time
from comments as c, user as u
where c.user_id_from = ? and c.user_id_to is not null and c.user_id_to = u.user_id



-- 获取回复我的评论
-- 通过game_id获取游戏名
select c.comment_id, u.user_name, bg.game_name, bg.game_belong, c.comment_time
from comments as c, user as u, base_game as bg
where c.user_id_to = ? and c.user_id_from = u.user_id and c.game_id = bg.game_id





-- 用户表
create table if not exists user(
	user_id int(11) auto_increment primary key,
	password varchar(18) not null,
	priority varchar(10) not null,
	fans_number int(11) default 0,
	logintime timestamp default current_timestamp(),
	user_name varchar(255) unique not null,
	phone varchar(11) unique,
	mail varchar(255) unique,
	status boolean not null,
	img varchar(255) default "http://localhost:8080/forum/images/avatar/default.jpg",
	follow_number int(11) default 0,
	sex varchar(20) default "未设置",
	birthdate date default '1970-01-01',		-- 1970-01-01 08:00:00
	index index_id(user_id)
)engine=InnoDB;


-- 关注表
-- check(main_userid <> fans_userid)  和外键冲突
-- 方法一：触发器
-- 方法二：客户端检测
-- 方法三：服务端检测
create table if not exists user_relationship(
	main_userid int(11) not null,			-- 爱豆的 user_id
	fans_userid int(11) not null,			-- 粉丝的 user_id
	primary key(main_userid, fans_userid),
	foreign key(main_userid) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
	foreign key(fans_userid) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE
)


-- 获取我的关注
select u.user_id, u.user_name, u.img
from user_relationship as ur, user as u
where ur.fans_userid = ? and ur.main_userid = u.user_id

-- 获取我的粉丝
select u.user_id, u.user_name, u.img
from user_relationship as ur, user as u
where ur.main_userid = ? and ur.fans_userid = u.user_id



-- 收藏表
create table if not exists collection(
	user_id int(11) not null,
	game_id varchar(255) not null,
	game_name varchar(255) not null,
	game_type varchar(255) not null,
	game_platform varchar(255) not null,
	game_belong varchar(255) not null,
	game_img varchar(255) not null,
	primary key(user_id,game_id),
	foreign key(user_id) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
	index index_id(user_id)
)engine=InnoDB;



-- 登录日志
create table if not exists login_log(
	user_id int(11) primary key,
	login_time date not null,
	foreign key(user_id) references user(user_id)
	ON DELETE CASCADE ON UPDATE CASCADE,
	index index_id(user_id)
)engine=InnoDB;



-- 游戏简介
-- 对于排行榜第一的game_id，单机:s1，安卓:a1，苹果:i1，网页:o1
			-- game_name, 单机:sr_game_name, 安卓: ar_game_name, 苹果: ir_game_name, 网页: or_game_name
-- 对于游戏名game_name, 单机:s_game_name, 安卓:a_game_name, 苹果:i_game_name, 网页:o_game_name
create table if not exists game_introduction(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null unique,
	`content` Text,
	index index_id(`game_id`)		-- 建立索引，优化
) engine=InnoDB;




-- 创建基本游戏表
create table if not exists base_game(
	`game_id` varchar(255) primary key,
	`game_name` varchar(255) not null,		-- 不设为 unqiue
	`game_belong` varchar(255) not null 	-- 单机游戏 | 安卓游戏 | 苹果游戏 | 网页游戏
)


-- 创建触发器日志表
/* create table if not exists trigger_log(
	`log_id` int(11) primary key auto_increment,
	`trigger_name` varchar(255) not null,
	`content` varchar(255) not null,
	`log_time` timestamp default current_timestamp()
) */


-- single_game 的触发器
-- single_game_insert
delimiter ||
create trigger single_game_insert 
after insert
on single_game for each row
begin 
	insert into base_game(game_id, game_name, game_belong)
		values (NEW.game_id, NEW.game_name, '单机游戏');
end ||
delimiter ;

-- single_game_update
delimiter ||
create trigger single_game_update
after update
on single_game for each row 
begin
	if NEW.game_name != OLD.game_name then 
		update base_game 
			set game_name = NEW.game_name
			where game_id = OLD.game_id;
	end if;
end ||
delimiter ;

-- single_game_delete
delimiter ||
create trigger single_game_delete
after delete
on single_game for each row
begin 
	delete from base_game
		where game_id = OLD.game_id;
end ||
delimiter ;



-- android_game 的触发器
-- android_game_insert
delimiter ||
create trigger android_game_insert 
after insert
on android_game for each row
begin 
	insert into base_game(game_id, game_name, game_belong)
		values (NEW.game_id, NEW.game_name, '安卓游戏');
end ||
delimiter ;

-- android_game_update
delimiter ||
create trigger android_game_update
after update
on android_game for each row 
begin
	if NEW.game_name != OLD.game_name then 
		update base_game 
			set game_name = NEW.game_name
			where game_id = OLD.game_id;
	end if;
end ||
delimiter ;

-- android_game_delete
delimiter ||
create trigger android_game_delete
after delete
on android_game for each row
begin 
	delete from base_game
		where game_id = OLD.game_id;
end ||
delimiter ;




-- ios_game 的触发器
-- ios_game_insert
delimiter ||
create trigger ios_game_insert 
after insert
on ios_game for each row
begin 
	insert into base_game(game_id, game_name, game_belong)
		values (NEW.game_id, NEW.game_name, '苹果游戏');
end ||
delimiter ;

-- ios_game_update
delimiter ||
create trigger ios_game_update
after update
on ios_game for each row 
begin
	if NEW.game_name != OLD.game_name then 
		update base_game 
			set game_name = NEW.game_name
			where game_id = OLD.game_id;
	end if;
end ||
delimiter ;

-- ios_game_delete
delimiter ||
create trigger ios_game_delete
after delete
on ios_game for each row
begin 
	delete from base_game
		where game_id = OLD.game_id;
end ||
delimiter ;




-- online_game 的触发器
-- online_game_insert
delimiter ||
create trigger online_game_insert 
after insert
on online_game for each row
begin 
	insert into base_game(game_id, game_name, game_belong)
		values (NEW.game_id, NEW.game_name, '网页游戏');
end ||
delimiter ;

-- online_game_update
delimiter ||
create trigger online_game_update
after update
on online_game for each row 
begin
	if NEW.game_name != OLD.game_name then 
		update base_game 
			set game_name = NEW.game_name
			where game_id = OLD.game_id;
	end if;
end ||
delimiter ;

-- online_game_delete
delimiter ||
create trigger online_game_delete
after delete
on online_game for each row
begin 
	delete from base_game
		where game_id = OLD.game_id;
end ||
delimiter ;
