DROP TABLE IF EXISTS "User" CASCADE;
DROP TABLE IF EXISTS Channel CASCADE;
DROP TABLE IF EXISTS Video CASCADE;
DROP TABLE IF EXISTS "Comment" CASCADE;
DROP TABLE IF EXISTS Playlist CASCADE;
DROP TABLE IF EXISTS Complaint CASCADE;
DROP TABLE IF EXISTS Post CASCADE;
DROP TABLE IF EXISTS LiveTranslation CASCADE;
DROP TABLE IF EXISTS Chat CASCADE;
DROP TABLE IF EXISTS Rate CASCADE;
DROP TABLE IF EXISTS "Subscription" CASCADE;
DROP TABLE IF EXISTS Tag_video CASCADE;
DROP TABLE IF EXISTS Tag CASCADE;
DROP TABLE IF EXISTS Playlist_video CASCADE;
-- SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE "User" (
    user_id SERIAL PRIMARY KEY,
    regDate DATE NOT NULL,
    surname VARCHAR(35) NOT NULL,
    "name" VARCHAR(35) NOT NULL,
    patronymic VARCHAR(35) NOT NULL,
    nick VARCHAR(30) NOT NULL,
    -- avatar IMAGE NOT NULL,
    email VARCHAR(254) NOT NULL,
    pass VARCHAR NOT NULL
);

CREATE TABLE Channel (
    channel_id SERIAL NOT NULL,
    owner_id INTEGER REFERENCES "User" (user_id),
    "name" VARCHAR(100) NOT NULL,
    subsCounter INTEGER NOT NULL,
    description VARCHAR(1000) NOT NULL,
    regDate DATE NOT NULL,
    -- avatar IMAGE NOT NULL,
    PRIMARY KEY (channel_id)
);

CREATE TABLE Video (
    video_id SERIAL NOT NULL,
    publisher_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    "name" VARCHAR(100) NOT NULL,
    publicationDate TIMESTAMP  NOT NULL,
    timeCodes TIME NOT NULL,
    description VARCHAR(5000) NOT NULL,
    likesCount INTEGER NOT NULL,
    dislikesCount INTEGER NOT NULL,
    "type" BOOLEAN NOT NULL,
    "length" TIME NOT NULL,
    PRIMARY KEY (video_id)
);

CREATE TABLE Post (
    post_id SERIAL NOT NULL,
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    text TEXT NOT NULL,
    -- media IMAGE NOT NULL,
    PRIMARY KEY (post_id)
);

CREATE TABLE "Comment" (
    comment_id SERIAL NOT NULL,
    parent_id INTEGER REFERENCES "Comment" (comment_id),
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    related_video_id INTEGER REFERENCES Video (video_id),
    related_post_id INTEGER REFERENCES Post (post_id),
--     relatedTo BOOLEAN NOT NULL,
    "content" TEXT NOT NULL,
    likesCount INTEGER NOT NULL,
    dislikesCount INTEGER NOT NULL,
    publicationDate TIMESTAMP NOT NULL,
    PRIMARY KEY (comment_id)
);

CREATE TABLE Playlist (
    playlist_id SERIAL NOT NULL,
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    video_id INTEGER NOT NULL REFERENCES Video (video_id),
    "name" VARCHAR(100) NOT NULL,
    lastChangeDate TIMESTAMP NOT NULL,
    viewsCount INTEGER NOT NULL,
    PRIMARY KEY (playlist_id)
);

CREATE TABLE Complaint (
    complaint_id SERIAL NOT NULL,
    video_id INTEGER NOT NULL REFERENCES Video (video_id),
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    PRIMARY KEY (complaint_id)
);

CREATE TABLE LiveTranslation (
    translation_id SERIAL NOT NULL,
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    audiensCount INTEGER NOT NULL,
    startTime TIMESTAMP NOT NULL,
    PRIMARY KEY (translation_id)
);

CREATE TABLE Chat (
    chat_id SERIAL NOT NULL,
    translation_id INTEGER NOT NULL REFERENCES LiveTranslation (translation_id),
    chanel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    messageText VARCHAR(100) NOT NULL,
    PRIMARY KEY (chat_id)
);

CREATE TABLE Rate (
    rate_id SERIAL NOT NULL,
    video_id INTEGER NOT NULL REFERENCES Video (video_id),
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    rate smallint NOT NULL,
    PRIMARY KEY (rate_id)
);

CREATE TABLE "Subscription" (
    subscription_id SERIAL NOT NULL,
    subscriptor_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    channel_id INTEGER NOT NULL REFERENCES Channel (channel_id),
    PRIMARY KEY (subscription_id)
);

CREATE TABLE Tag (
    tag_id SERIAL NOT NULL,
    "name" VARCHAR(100) NOT NULL,
    PRIMARY KEY (tag_id)
);

CREATE TABLE Tag_video (
    tag_video_id SERIAL NOT NULL,
    video_id INTEGER NOT NULL REFERENCES Video (video_id),
    tags_id INTEGER NOT NULL REFERENCES Tag (tag_id),
    PRIMARY KEY (tag_video_id)
);

CREATE TABLE Playlist_video (
    playlist_video_id SERIAL NOT NULL,
    playlist_id INTEGER NOT NULL REFERENCES Playlist (playlist_id),
    video_id INTEGER NOT NULL REFERENCES Video (video_id),
    PRIMARY KEY (playlist_video_id)
);
