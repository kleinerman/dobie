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



CREATE TABLE `ResState` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(20) NOT NULL
)
;

CREATE TABLE `Organization` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `resStateId` integer NOT NULL
)
;

CREATE TABLE `Person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `identNumber` varchar(40) NOT NULL,
    `cardNumber` integer NOT NULL,
    `orgId` integer,
    `visitedOrgId` integer,
    `resStateId` integer NOT NULL,
    CONSTRAINT `fk_Person_Organization` FOREIGN KEY (`orgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fk_Person_VisitedOrganization` FOREIGN KEY (`visitedOrgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fk_Person_ResState` FOREIGN KEY (`resStateId`) REFERENCES `ResState` (`id`)
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
    `doorsQuant` integer NOT NULL
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


CREATE TABLE `Door` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `doorNum` integer NOT NULL,
    `name` varchar(40) NOT NULL,
    `controllerId` integer NOT NULL,
    `rlseTime` integer NOT NULL,
    `bzzrTime` integer NOT NULL,
    `alrmTime` integer NOT NULL,
    `zoneId` integer NOT NULL,
    `isVisitExit` boolean NOT NULL,
    `resStateId` integer NOT NULL,
    CONSTRAINT `fk_Door_Controller` FOREIGN KEY (`controllerId`) REFERENCES `Controller` (`id`),
    CONSTRAINT `fk_Door_Zone` FOREIGN KEY (`zoneId`) REFERENCES `Zone` (`id`),
    CONSTRAINT `fk_Door_ResState` FOREIGN KEY (`resStateId`) REFERENCES `ResState` (`id`)
)
;

CREATE UNIQUE INDEX CtrllerDoorNumIndex ON Door (controllerId, doorNum)
;

CREATE TABLE `VisitDoorGroup` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL
)
;

CREATE TABLE `VisitDoorGroupDoor` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `visitDoorGroupId` integer NOT NULL,
    `doorId` integer NOT NULL,
    CONSTRAINT `fk_VisitDoorGroupDoor_VisitDoorGroup` FOREIGN KEY (`visitDoorGroupId`) REFERENCES `VisitDoorGroup` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_VisitDoorGroupDoor_Door` FOREIGN KEY (`doorId`) REFERENCES `Door` (`id`) ON DELETE CASCADE
)
;

CREATE UNIQUE INDEX VisitDoorGroupDoorIndex ON VisitDoorGroupDoor (visitDoorGroupId, doorId)
;




CREATE TABLE `Access` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `doorId` integer NOT NULL,
    `personId` integer NOT NULL,
    `allWeek` boolean NOT NULL,
    `iSide` boolean NOT NULL,
    `oSide` boolean NOT NULL,
    `startTime` time,
    `endTime` time,
    `expireDate` date NOT NULL,
    `resStateId` integer NOT NULL,
    CONSTRAINT `fk_Access_Door` FOREIGN KEY (`doorId`) REFERENCES `Door` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Access_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Access_ResState` FOREIGN KEY (`resStateId`) REFERENCES `ResState` (`id`)
)
;

CREATE UNIQUE INDEX doorPersonIndex ON Access (doorId, personId)
;

CREATE TABLE `LimitedAccess` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `doorId` integer NOT NULL,
    `personId` integer NOT NULL,
    `weekDay` integer NOT NULL,
    `iSide` boolean NOT NULL,
    `oSide` boolean NOT NULL,
    `startTime` time NOT NULL,
    `endTime` time NOT NULL,
    `resStateId` integer NOT NULL,
    CONSTRAINT `fk_LimitedAccess_Door` FOREIGN KEY (`doorId`) REFERENCES `Door` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_LimitedAccess_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_LimitedAccess_ResState` FOREIGN KEY (`resStateId`) REFERENCES `ResState` (`id`))
;

CREATE UNIQUE INDEX doorPersonWeekDayIndex ON LimitedAccess (doorId, personId, weekDay)
;



CREATE TABLE `EventType` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL
)
;

CREATE TABLE `DoorLock` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL
)
;

CREATE TABLE `DenialCause` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL
)
;

CREATE TABLE `Event` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `eventTypeId` integer NOT NULL,
    `doorId` integer NOT NULL,
    `dateTime` datetime NOT NULL,
    `doorLockId` integer,
    `personId` integer,
    `side` boolean,
    `allowed` boolean,
    `denialCauseId` integer,
    CONSTRAINT `fk_Event_EventType` FOREIGN KEY (`eventTypeId`) REFERENCES `EventType` (`id`),
    CONSTRAINT `fk_Event_Door` FOREIGN KEY (`doorId`) REFERENCES `Door` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Event_DoorLock` FOREIGN KEY (`doorLockId`) REFERENCES `DoorLock` (`id`),    
    CONSTRAINT `fk_Event_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_Event_DenialCause` FOREIGN KEY (`denialCauseId`) REFERENCES `DenialCause` (`id`)

)
;

CREATE TABLE `PersonPendingOperation` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `personId` integer NOT NULL,
    `macAddress` varchar(12) NOT NULL,
    `pendingOp` integer NOT NULL,
    CONSTRAINT `fk_PersonPendingOperation_Person` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fk_PersonPendingOperation_ResState` FOREIGN KEY (`pendingOp`) REFERENCES `ResState` (`id`)

)
;

CREATE UNIQUE INDEX personMacAddressIndex ON PersonPendingOperation (personId, macAddress)
;



COMMIT;


