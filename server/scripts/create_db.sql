BEGIN;
CREATE TABLE `Company` (
    `code` varchar(4) NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `webUser` varchar(40) NOT NULL,
    `rowState` varchar(1) NOT NULL
)
;
CREATE TABLE `CallCategory` (
    `code` varchar(3) NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowState` varchar(1) NOT NULL
)
;
CREATE TABLE `PhoneUser_callCategory` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `phoneuser_id` integer NOT NULL,
    `callcategory_id` varchar(3) NOT NULL,
    UNIQUE (`phoneuser_id`, `callcategory_id`)
)
;
COMMIT;

