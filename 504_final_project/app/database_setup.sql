/***********************************
  Database Setup Script
  **************************/


CREATE TABLE IF NOT EXISTS `SAVED_RESPONSES` (
    `ResponseData` TEXT NOT NULL,
    `AiResponseID` INT AUTO_INCREMENT NOT NULL,
    `RequestDate` DATETIME NOT NULL,
    `UserInquiry` TEXT NOT NULL,
    `INI` VARCHAR(255) NOT NULL,
    PRIMARY KEY (`AiResponseID`, `INI`)
);



CREATE TABLE IF NOT EXISTS `SQL_SNIPPETS` (
    `SnippetID` INT AUTO_INCREMENT NOT NULL,
    `INI` VARCHAR(255) NOT NULL,
    `Item_Number` VARCHAR(255) NOT NULL,
    `Description` TEXT NOT NULL,
    `SQLCode` TEXT NOT NULL,
    `CreatedDate` DATETIME NULL,
    PRIMARY KEY (`SnippetID`, `INI`, `Item_Number`)
);

CREATE TABLE IF NOT EXISTS `EPIC_LINKS` (
    `LinkID` INT AUTO_INCREMENT NOT NULL,
    `INI` VARCHAR(255) NOT NULL,
    `Item_Number` VARCHAR(255) NOT NULL,
    `Description` TEXT NOT NULL,
    `URL` TEXT NOT NULL,
    `CreatedDate` DATETIME NOT NULL,
    PRIMARY KEY (`LinkID`, `INI`, `Item_Number`)
);

 
-- Add Indexes for performance optimization
CREATE INDEX IDX_SAVED_RESPONSES_INI ON [SAVED_RESPONSES](INI);
CREATE INDEX IDX_SQL_SNIPPETS_INI_ITEM ON [SQL_SNIPPETS](INI, Item_Number);
CREATE INDEX IDX_EPIC_LINKS_INI_ITEM ON [EPIC_LINKS](INI, Item_Number);

-- Add Primary Keys
ALTER TABLE SAVED_RESPONSES ADD CONSTRAINT PK_SAVED_RESPONSES PRIMARY KEY CLUSTERED (AiResponseID, INI);
ALTER TABLE SQL_SNIPPETS ADD CONSTRAINT PK_SQL_SNIPPETS PRIMARY KEY CLUSTERED (SnippetID, INI, Item_Number)
ALTER TABLE EPIC_LINKS ADD CONSTRAINT PK_EPIC_LINKS PRIMARY KEY CLUSTERED (LinkID, INI, Item_Number); 


-- Add Primary Keys
ALTER TABLE `SAVED_RESPONSES` ADD CONSTRAINT PK_SAVED_RESPONSES PRIMARY KEY (`AiResponseID`, `INI`);
ALTER TABLE `SQL_SNIPPETS` ADD CONSTRAINT PK_SQL_SNIPPETS PRIMARY KEY (`SnippetID`, `INI`, `Item_Number`);
ALTER TABLE `EPIC_LINKS` ADD CONSTRAINT `PK_EPIC_LINKS` PRIMARY KEY (`LinkID`, `INI`, `Item_Number`);

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON epicReference.* TO 'app-user';
GO

-- insert sample data into the SQL_SNIPPETS table
INSERT INTO `SQL_SNIPPETS` (`INI`, `Item_Number`, `Description`, `SQLCode`, `CreatedDate`) VALUES ('DEP', '40', 'Department Practice abbreviation', 'SELECT DEPT_ABBREVIATION FROM CLARITY_DEP', '2023-01-01 00:00:00');
INSERT INTO `SQL_SNIPPETS` (`INI`, `Item_Number`, `Description`, `SQLCode`, `CreatedDate`) VALUES ('EPT', '30', 'Patient encounter type', 'SELECT ENC_TYPE_C FROM PAT_ENC', '2023-01-02 00:00:00');
INSERT INTO `SQL_SNIPPETS` (`INI`, `Item_Number`, `Description`, `SQLCode`, `CreatedDate`) VALUES ('SER', '9301', 'provider MPIs', 'SELECT IDENTITY_TYPE_ID FROM IDENTITY_SER_ID', '2023-01-03 00:00:00');
 -- insert sample data into the EPIC_LINKS table
INSERT INTO `EPIC_LINKS` (`INI`, `Item_Number`, `Description`, `URL`, `CreatedDate`) VALUES ('DEP', '40', 'Department Practice abbreviation', 'https://datahandbook.epic.com/ClarityDictionary/Details?tblName=CLARITY_DEP', '2023-01-01 00:00:00');
INSERT INTO `EPIC_LINKS` (`INI`, `Item_Number`, `Description`, `URL`, `CreatedDate`) VALUES ('EPT', '30', 'Patient address', 'https://datahandbook.epic.com/ClarityDictionary/Details?tblName=PAT_ENC', '2023-01-02 00:00:00');
INSERT INTO `EPIC_LINKS` (`INI`, `Item_Number`, `Description`, `URL`, `CreatedDate`) VALUES ('SER', '9301', 'provider MPIs', 'https://datahandbook.epic.com/ClarityDictionary/Details?tblName=IDENTITY_SER_ID', '2023-01-03 00:00:00');


-- End of Database Setup Script