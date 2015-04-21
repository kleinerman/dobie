BEGIN;
CREATE TABLE `Person` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `cardNumber` integer NOT NULL,
    `orgId` integer NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkOrgId` FOREIGN KEY (`orgId`) REFERENCES `Organization` (`id`),
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Organization` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
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
    CONSTRAINT `fkZoneId` FOREIGN KEY (`zoneId`) REFERENCES `Zone` (`id`),
    CONSTRAINT `fkControllerId` FOREIGN KEY (`controllerId`) REFERENCES `Controller` (`id`),
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Zone` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `name` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Controller` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `boardModel` varchar(40) NOT NULL,
    `ip` varchar(40) NOT NULL
)
;


CREATE TABLE `Access` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgId` integer NOT NULL,
    `personId` integer NOT NULL,
    `allWeek` bool NOT NULL,
    `iSide` bool NOT NULL,
    `oSide` bool NOT NULL,
    `startTime` time,
    `endTime` time,
    `expireDate` date NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkPssgId` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fkPersonId` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;


CREATE TABLE `LimitedAccess` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pssgId` integer NOT NULL,
    `personId` integer NOT NULL,
    `allWeek` bool NOT NULL,
    `iSide` bool NOT NULL,
    `oSide` bool NOT NULL,
    `weekDay` integer NOT NULL,
    `startTime` time NOT NULL,
    `endTime` time NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkPssgId` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fkPersonId` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`),
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Event` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `eventTypeId` integer NOT NULL,
    `pssgId` integer NOT NULL,
    `dateTime` datetime NOT NULL,
    `latchId` integer,
    `personId` integer,
    `side` bool,
    `allowed` bool,
    `notReason` integer,
    CONSTRAINT `fkEventTypeId` FOREIGN KEY (`eventTypeId`) REFERENCES `EventType` (`id`),
    CONSTRAINT `fkPssgId` FOREIGN KEY (`pssgId`) REFERENCES `Passage` (`id`),
    CONSTRAINT `fkLatchId` FOREIGN KEY (`latchId`) REFERENCES `Latch` (`id`),    
    CONSTRAINT `fkPersonId` FOREIGN KEY (`personId`) REFERENCES `Person` (`id`)


)
;

CREATE TABLE `EventType` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `Latch` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `NotReason` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL,
    `rowStateId` integer NOT NULL,
    CONSTRAINT `fkRowStateId` FOREIGN KEY (`rowStateId`) REFERENCES `RowState` (`id`)
)
;

CREATE TABLE `RowState` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `description` varchar(40) NOT NULL
)
;
COMMIT;

