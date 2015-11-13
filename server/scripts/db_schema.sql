BEGIN;

CREATE TABLE `RowState` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(20) NOT NULL
)
;

CREATE TABLE `Organization` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL
)
;

CREATE TABLE `Person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `cardNumber` integer NOT NULL,
    `orgId` integer NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Person_Organization` FOREIGN KEY (`orgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fk_Person_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Controller` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `boardModel` varchar(40) NOT NULL,
    `macAddress` varchar(12) NOT NULL,
    `ipAddress` varchar(39) NOT NULL
)
;

CREATE TABLE `Zone` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL
)
;

CREATE TABLE `Passage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `i0In` integer NOT NULL,
    `i1In` integer NOT NULL,
    `o0In` integer NOT NULL,
    `o1In` integer NOT NULL,
    `bttnIn` integer NOT NULL,
    `stateIn` integer NOT NULL,
    `rlseOut` integer NOT NULL,
    `bzzrOut` integer NOT NULL,
    `zoneId` integer NOT NULL,
    `controllerId` integer NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Passage_Controller` FOREIGN KEY (`controllerId`) REFERENCES `Controller` (`id`),
    CONSTRAINT `fk_Passage_Zone` FOREIGN KEY (`zoneId`) REFERENCES `Zone` (`id`),
    CONSTRAINT `fk_Passage_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Access` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgId` integer NOT NULL,
    `personId` integer NOT NULL,
    `allWeek` boolean NOT NULL,
    `iSide` boolean NOT NULL,
    `oSide` boolean NOT NULL,
    `startTime` time,
    `endTime` time,
    `expireDate` date NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Access_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fk_Access_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fk_Access_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;


CREATE TABLE `LimitedAccess` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgId` integer NOT NULL,
    `personId` integer NOT NULL,
    `iSide` boolean NOT NULL,
    `oSide` boolean NOT NULL,
    `weekDay` integer NOT NULL,
    `startTime` time NOT NULL,
    `endTime` time NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_LimitedAccess_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fk_LimitedAccess_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fk_LimitedAccess_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`))
;

CREATE TABLE `EventType` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_EventType_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Latch` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Latch_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `NotReason` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_NotReason_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Event` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `eventTypeId` integer NOT NULL,
    `pssgId` integer NOT NULL,
    `dateTime` datetime NOT NULL,
    `latchId` integer,
    `personId` integer,
    `side` boolean,
    `allowed` boolean,
    `notReason` integer,
    CONSTRAINT `fk_Event_EventType` FOREIGN KEY (`eventTypeId`) REFERENCES `EventType` (`id`),
    CONSTRAINT `fk_Event_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fk_Event_Latch` FOREIGN KEY (`latchId`) REFERENCES `Latch` (`id`),    
    CONSTRAINT `fk_Event_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fk_Event_NotReason` FOREIGN KEY (`notReason`) REFERENCES `NotReason` (`id`)

)
;

COMMIT;


