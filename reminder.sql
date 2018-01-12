CREATE TABLE user
(
  user_name  VARCHAR(20) NULL,
  user_psw   VARCHAR(10) NULL,
  user_email VARCHAR(30) NOT NULL
    PRIMARY KEY,
  token      VARCHAR(1)  NOT NULL
);


CREATE TABLE event
(
  user_email  VARCHAR(30)            NOT NULL,
  reminder    VARCHAR(15)            NOT NULL,
  title       VARCHAR(20)            NOT NULL,
  record      VARCHAR(100)           NOT NULL,
  update_time DATETIME               NULL,
  alarm_time  DATETIME               NULL,
  action_time DATETIME               NULL,
  if_alarm    VARCHAR(1) DEFAULT '0' NOT NULL,
  if_email    VARCHAR(1) DEFAULT '0' NOT NULL,
  CONSTRAINT PRIMARY KEY( `user_email`, `reminder`)
);
