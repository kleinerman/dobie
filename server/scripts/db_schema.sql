BEGIN;

CREATE TABLE `Role` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(20) NOT NULL
)
;

CREATE TABLE `User` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(64) NOT NULL,
    `username` varchar(32) NOT NULL,
    `passwdHash` varchar(128) NOT NULL,
    `roleId` integer NOT NULL,
    CONSTRAINT `fk_User_Role` FOREIGN KEY (`roleId`) REFERENCES `Role` (`id`)
)
;

CREATE UNIQUE INDEX usernameIndex ON User (username)
;



CREATE TABLE `RowState` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(20) NOT NULL
)
;

CREATE TABLE `Organization` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL
)
;

CREATE TABLE `Person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `identNumber` varchar(40) NOT NULL,
    `cardNumber` integer NOT NULL,
    `orgId` integer,
    `visitedOrgId` integer,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Person_Organization` FOREIGN KEY (`orgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fk_Person_VisitedOrganization` FOREIGN KEY (`visitedOrgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fk_Person_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE UNIQUE INDEX cardNumberIndex ON Person (cardNumber)
;
CREATE UNIQUE INDEX identNumberIndex ON Person (identNumber)
;


CREATE TABLE `CtrllerModel` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `boardModel` varchar(40) NOT NULL,
    `pssgsQuant` integer NOT NULL
)
;


CREATE TABLE `Controller` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ctrllerModelId` integer NOT NULL,
    `macAddress` varchar(12) NOT NULL,
    `ipAddress` varchar(39),
    CONSTRAINT `fk_Controller_CtrllerModel` FOREIGN KEY (`ctrllerModelId`) REFERENCES `CtrllerModel` (`id`)
)
;

CREATE UNIQUE INDEX macAddressIndex ON Controller (macAddress)
;



CREATE TABLE `Zone` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL
)
;


CREATE TABLE `Passage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgNum` integer NOT NULL,
    `description` varchar(40),
    `controllerId` integer NOT NULL,
    `rlseTime` integer NOT NULL,
    `bzzrTime` integer NOT NULL,
    `alrmTime` integer NOT NULL,
    `zoneId` integer NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_Passage_Controller` FOREIGN KEY (`controllerId`) REFERENCES `Controller` (`id`),
    CONSTRAINT `fk_Passage_Zone` FOREIGN KEY (`zoneId`) REFERENCES `Zone` (`id`),
    CONSTRAINT `fk_Passage_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE UNIQUE INDEX CtrllerPssgNumIndex ON Passage (controllerId, pssgNum)
;

CREATE TABLE `VisitorsPassages` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL
)
;

CREATE TABLE `VisitorsPassagesPassage` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `visitorsPssgsId` integer NOT NULL,
    `pssgId` integer NOT NULL,
    CONSTRAINT `fk_VisitorsPassagesPassage_VisitorsPassages` FOREIGN KEY (`visitorsPssgsId`) REFERENCES `VisitorsPassages` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_VisitorsPassagesPassage_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`) ON DELETE CASCADE
)
;

CREATE UNIQUE INDEX VisitorsPassagesPassageIndex ON VisitorsPassagesPassage (visitorsPssgsId, pssgId)
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
    CONSTRAINT `fk_Access_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Access_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Access_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE UNIQUE INDEX pssgPersonIndex ON Access (pssgId, personId)
;

CREATE TABLE `LimitedAccess` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgId` integer NOT NULL,
    `personId` integer NOT NULL,
    `weekDay` integer NOT NULL,
    `iSide` boolean NOT NULL,
    `oSide` boolean NOT NULL,
    `startTime` time NOT NULL,
    `endTime` time NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fk_LimitedAccess_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_LimitedAccess_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_LimitedAccess_RowState` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`))
;

CREATE UNIQUE INDEX pssgPersonWeekDayIndex ON LimitedAccess (pssgId, personId, weekDay)
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
    `notReasonId` integer,
    CONSTRAINT `fk_Event_EventType` FOREIGN KEY (`eventTypeId`) REFERENCES `EventType` (`id`),
    CONSTRAINT `fk_Event_Passage` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Event_Latch` FOREIGN KEY (`latchId`) REFERENCES `Latch` (`id`),    
    CONSTRAINT `fk_Event_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Event_NotReason` FOREIGN KEY (`notReasonId`) REFERENCES `NotReason` (`id`)

)
;

CREATE TABLE `PersonPendingOperation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `personId` integer NOT NULL,
    `macAddress` varchar(12) NOT NULL,
    `pendingOp` integer NOT NULL,
    CONSTRAINT `fk_PersonPendingOperation_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fk_PersonPendingOperation_RowState` FOREIGN KEY (`pendingOp`) REFERENCES `RowState` (`id`)

)
;

CREATE UNIQUE INDEX personMacAddressIndex ON PersonPendingOperation (personId, macAddress)
;



COMMIT;


