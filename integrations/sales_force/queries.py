ACCOUNT_QUERY = """SELECT Id, Name, Type, AccountNumber, Industry,
                AnnualRevenue, Rating, NumberOfEmployees, Website, Ownership, CreatedDate, 
                LastModifiedDate FROM Account"""


BILLING_QUERY = """ SELECT 
                    Id, FirstName, LastName, Email, Phone, MobilePhone, MailingStreet, MailingCity, MailingState, MailingPostalCode,
                    MailingCountry, AccountId, CreatedDate, LastModifiedDate,Languages__c
                FROM CONTACT """