       
        
        
-- ******* Process UPDATE,INSERT & DELETE simultaneously  ********                
        
    
        

   
        
merge into SALES_FINAL_TABLE F      -- Target table to merge changes from source table
USING ( SELECT STRE.*,ST.location,ST.employees
        FROM SALES_STREAM STRE
        JOIN STORE_TABLE ST
        ON STRE.store_id = ST.store_id
       ) S
ON F.id=S.id
when matched                        -- DELETE condition
    and S.METADATA$ACTION ='DELETE' 
    and S.METADATA$ISUPDATE = 'FALSE'
    then delete                   
when matched                        -- UPDATE condition
    and S.METADATA$ACTION ='INSERT' 
    and S.METADATA$ISUPDATE  = 'TRUE'       
    then update 
    set f.product = s.product,
        f.price = s.price,
        f.amount= s.amount,
        f.store_id=s.store_id
when not matched 
    and S.METADATA$ACTION ='INSERT'
    then insert 
    (id,product,price,store_id,amount,employees,location)
    values
    (s.id, s.product,s.price,s.store_id,s.amount,s.employees,s.location);
        




SELECT * FROM SALES_RAW_STAGING;     
        
SELECT * FROM SALES_STREAM;

SELECT * FROM SALES_FINAL_TABLE;
       

       
       



INSERT INTO SALES_RAW_STAGING VALUES (2,'Lemon',0.99,1,1);




UPDATE SALES_RAW_STAGING
SET PRODUCT = 'Lemonade'
WHERE PRODUCT ='Lemon';



       
DELETE FROM SALES_RAW_STAGING
WHERE PRODUCT = 'Lemonade';       


--- Example 2 ---

INSERT INTO SALES_RAW_STAGING VALUES (10,'Lemon Juice',2.99,1,1);

UPDATE SALES_RAW_STAGING
SET PRICE = 3
WHERE PRODUCT ='Mango';
       
DELETE FROM SALES_RAW_STAGING
WHERE PRODUCT = 'Potato';    

