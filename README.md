
# Snowflake Cloud

### Loading Data Diff Ways ###

    1. Diff loads and stages
    2. Create or replace stage with URL and creds
    3. Alter stage
    4. Desc stage
    5. List files under stage
    6. Copy into table with options like read from stage, file format, read spec files, read with pattern
    7. Copy into table with options like select spec columns from stage, do case and substrings trmtns
    8. Load only spec columns by passing column names
    9. Set auto incremental value for each record.
        For ex: profit as int but values coming as text
    10. Copy with on_error as continue
    11. Copy with on_error as abort_statement - nothing will be loaded (default)
    12. Copy with on_error as skip_file
    13. Copy with on_error as skip_file_2; load the file error count in a file <2 else skip if it is 2 or >2 
    14. Copy with on_error as skip_file_0.5; if 0.5% of the total rows have an error then the file will be skipped
    15. Create file format object. (Default is csv type)
    16. Alter file format (set SKIP_HEADER=1) //file type can't be altered


### Copy With options ###
    Copy Options - helps us to validate before loading

    1. Return 10 rows if no errors else return errors - validation_mode as RETURN_ERRORS or RETURN_10_ROWS – return_errors will give error and rejected_record
    2. Select rejected_record from table (result_scan(last_query_id())) and apply split_part to retrieve individual columns.
    3. Size_limit in bytes - first file will always be loaded. When the threshold meets, it will stop copying.
    4. return_failed_only=true with on_error=continue will show both loaded or partially loaded files
    5. Truncatecolumns=true - strings are automatically truncated to the target column length.
    6. force=true | reload the same file again - potentially duplicating data in a table
    7. INFORMATION_SCHEMA.LOAD_HISTROY table - can lookup table load history 
    8. We can also see global load_history details of a table from snowflake.account_usage._load_history like if someone recreated the table with same name also can filter date(last_load_date) <= dateadd(days, -1, current_date)


### Handle JSON and Parquet Data ###
    Json:-

    1. Create statge, file format and using copy cmd, load the raw json data into a table with one column (raw_file) and its type as variant datatype.
    2. Refer spec using raw_file:city from tblname for better style use raw_file:first_name::string as first_name from tblname.
    3. If we have nested data in a column called job then do raw_file:job.salary::int as salary to get salary column from job nested data. Similarly for others columns like raw_file.job.title::string as job_title from tblname.
    4. if we have array type column like prev_company then do raw_file:prev_company[1]::string as prev_company or raw_file:prev_company[0]::string
    5. To get a size of an array then do ARRAY_SIZE (raw_file:prev_company) from tblname.
    6. if we have array with nested data in it then do raw_file:languages_spoken[0].language::string as first_language and raw_file.languages_spoken[0].level::string as level_spoken from tblname and use union all to get elements from 2nd and 3rd elements of array assuming the person may be speaking multiple languages. And finally we can use table with flatten function.
    7. select raw_file:first_name::string as first_name, f.value:language::string as first_language, f.value.level:string as level_spoken from tblname table(flatten(raw_file:spoken_languages)) f;

    Parquet:-

    1. create file format object with type as parquet
    2. Create stage and mention file format created above. Here column name will come as $1
    3. Select 
            $1:__index_level_0__::int as index_level,
            $1:cat_id::varchar (50) as category,
            Date ($1: date::int) as date,
            $1:dept_id::varchar(50) as dept_id, $1:store_id::varchar(50) as store_id,
            $1:item_id::varchar(50) as item_id , metadata$file_name as file_name
        metadata$file_row_number as rownumber
        to_timestamp_ntz (current_timestamp) as load_date from stage

    


### Performance Tunning ###

    1. traditional - creating indexes, PKs, partitions, bucketing, avoid full table scans.
    2. dedicated warehouses - spreading as per diff workloads(batch, ML, Adhoc, reporting, streaming) 
    3. scale up- for known patterns of high work load | for complex queries (increasing the size of exisitng warehouse) 
    4. scale out- dynamically for unknown patterns of high work load | for concurrent uses (adding more warehouses and clusters) 
    5. maximize cache usage- automatic caching can be maximized | results of the query are automatically cached results are cached for 24 hrs or untill underlying data has changed. ensure similar queries go on the same warehouse. 
    6. cluster key- for large tables | its more like a range partition | this is automated by snowflake.
    7. clustering is not for all tables
    8. mainly very large tables of multiple TBs of data.
    9. we can also specify cluster by columns when creating tables.


 ### Loading from AWS ###

    1. create an aws account, s3 bucket (same region as snowflake) and upload files.
    2. create an IAM role with type as other aws account and attach s3 related policies
    3. create storage integration object in snowflake providing s3 related info like iam arn and storage allowed locations (buckets)(create or replace storage integration s3_int)
    4. once we create this do desc on storage integration object (s3_int). 
    5. copy the value of STORAGE_AWS_IAM_USER_ARN and STORAGE_AWS_EXTERNAL_ID and go to the role in aws and add these in trusted relationship.
    6. create file_format; empty_field_as_null=true, fields_optionally_enclosed_by=’”’, null_if(‘NULL’, ‘null’)
    7. create stahe with integration object
    8. then use copy command to load the data from stage object



### Snowpipe ###

    1. create pipe auto_ingest=true as copy cmnd
    2. alter pipe pipename refresh
    3. desc pipe pipename and copy the value of notificaion_channel
    4. goto s3 bucket and create event trigger for the pipe in properties tab
    5. create event notification - all object create event, select dest as sqs queue with arn and give value of notificaion_channel
    6. verify if the pipe is working - select system$pipe_status('pipename') - unfortunately, this will not show an error though there is an issue.
    7. use below to check the actual error from snowpipe - gives standard error message
        select *from table(validate_pipe_load(
        pipe_name => 'emp_pipe'
        start_time => dateadd(hour, -2, current_timestamp())))
    8. use below to get error message from table copy history - gives more accurate error
        select *from table(information_Schema.copy_history(
        table_name => 'tblname'
        start_time => dateadd(hour, -2, current_timestamp())))

### Manage Pipes ###

     1. desc pipe pipename;
     2. show pipes;
     3. show pipes like '%employee%'
     4. show pipes in database manage_db
     5. show pipes in schema manage_db.pipes
     6. show pipes like '%employee%' in database manage_db
     7. alter pipe db.schema.pipename set pipe_execution_paused = true


### Time Travel ###

    1. data deleted or updated by mistake so we can use time travel to restore.
    2. travel back upto 90 days using at , before and querid keywords. we can alter this value upto 90. can specify this when creating the table.
    3. if it is set to 0 for a table, timetravel will not work at all so we can't do undrop as well.
    4. there is a cost associated with time travel as we are using the more storage.
    5. select *from table at (OFFSET => 60*1.5) //travel back 1 and half min
    6. select *From table before (timestamp = > '2024-01-29 14:43:49.581::timestamp)
    7. select *From table before (statement = > 'queryid') //can get it from query history
    8. create or replace table as select *From table before (statement = > 'queryid') //restore but timetravel will not work as we recreated the table.
    9. instead truncate the table, load the data of time travel query to backup table
    10. load the main table from backup table.use below.
    11. create or replace tablebkp as select *From table before (statement = > 'queryid').
    12. truncate table maintablename
    13. insert into maintablename select *from tablebkp


### Undrop and Fail Safe ###

    1. if we drop the table by mistake.
    2. drop table tablename; undrop table tablename;
    3. drop schema schemname; 
    4. undrop schema schemname; samething goes with database.
    5. protection of historical data in case of disaster
    6. non-configurable 7-day period for permanent tables and 0 days for transient tables
    7. period starts immediately after time travel period ends.
    8. no user intervention and recoverable only by snowflake.
    9. contributes to storage cost. failsafe << time travel << current data storage


### Table Types ###
    1. permanent table (default)
	2. permanent data; exists untill dropped; time travel retention period (0 - 90 day)     
    3. fail safe
    4. transient table - data that does not need to be protected; create transient table;  
    5. exists until dropped; time travel retention period (0-1 day); no fail safe
    6. temporary table - data needed for a session; create temporary table; exists only in a session; 
    7. time travel retention period (0-1 day); 
    8. no fail safe
    9. types are also available for other database objects like databases and schemas
    10. if we create a temp schema and create tables inside the schema, all the tables 
    11. created inside the schema are temp tables.
    12. for temp table no naming conflicts with permanent/transient tables.
        meaning, if we have both permanent and temp table with same name in a session, our queries will run on temp table and not on permanent table.


### Zero-copy Cloning ###

    1. create copies of a db, a schema or a table. metadata will be automatically copied over.
    2. cloned object is independent from original table.
    3. there wont be any extra storage cost if we clone but there will be a cost if we    make any changes to the data in the cloned object.
    4. purpose - create backups for dev activities.
    5. works with time travel also
    6. create table tblname clone <src_tbl_name> before (timestamp => <timestamp>)


### swapping tables: swaps the data and metadata ###

    1. dev table into production table
    2. alter table tblname swap with <target_tbl_name>
    3. alter schema tblname swap with <target_schema_name>


### Data Sharing ###

    1. Data sharing without actual copy of the data & uptodate
    2. shared data can be consumed by the own compute resources
    3. non-snowflake users can also access through a reader account.
    4. we can create a share for snowflake users
    5. create a share object (create or replace share share_name)
        grant usage on database to share (grant usage on database dbname to share share_name)
        grant usage on schema to share (grant usage on schema schemaname to share share_name)
        grant select on view (grant select on view viewname to share share_name)
        add accoutn to share (alter share share_name add account=<acname>
        create database from share. inside we will see the view that we shared.
        create a reader account for non-snowflake-users; create a managed account with uname and password. this will give us the url.
    6. view vs secure view - view is nothing but saved sql
    7. secure view - if we want to hide the view def like tables, columns and where clauses.

### Tasks ###

    1. tasks can be scheduled sql statements.
    2. standalone tasks and tree of tasks.
    3. show tasks;
    4. alter task task_name set schedule='2 MINUTE'
    5. alter task cus_insert resume; /start
    6. alter task cus_insert suspend; /suspend
    7. create or replace task cus_insert
            warehouse='name'
            schedule='1 MINUTE'
            as
            into customers(create_date) values(current_timestamp)
    8.  CRON notation 
        * - minutes (0 - 59)
        * - hour (0 -23)
        * - day of month (0-31)
        * - month (0-12 JAN-DEC)
        * - day of week (0-6, SUN, SAT))

        create or replace task cus_insert1
        warehouse='name'
        schedule='USING CRON * * * * * UTC'
        as
        insert into customers(create_date) values(current_timestamp)
    9. create dependency - create tree of tasks using ADD AFTER <parent_task>
    10. create or replace task cus_insert2
        warehouse='name'
        add after cus_insert1
        as
        insert into customers(create_date) values(current_timestamp)
    11. if we dependent tasks, then we need to first start child tasks then at the end parent task
    12. dependency on streams.
        create or replace task cus_insert1
            warehouse='name'
            schedule='1 MINUTE'
            when system$stream_has_data('stream name')
            as
            insert into customers(create_date) values(current_timestamp)

### Streams ###
    1. streams: object in snowflake
    2. capture what has changed in source and make same changes in the target.
    3. create a stream on top of source table. and changed data will be in the stream object.
    4. we are not paying anything extra to the data in the stream object as this is more of replica of source but to the few metadata columns.
    5. create and load src table 
    6. insert into tgt table from src table
    7. create stream stream_name on table src_tblname; select *from stream;
    8. make changes to src_tblname; verify the same in stream
    9. if it is insert, metadata$action column will show as insert, metadata$update will show as false and the corresponding metadata$row_id
    10. if it is update, metadata$action column will show as update for new record and delete for old record,metadata$update will show as true and the corresponding metadata$row_id
    11. insert into tgt_table from stream_object; as soon as we load the data into tgt table, stream object will become empty
    12. update case: if it is update, metadata$action column will show as insert for new record and delete for old record,metadata$update will show as true and the corresponding metadata$row_id

        merge into tgt_table f 
        using stream_object s
        on f.id = s.id
        when matched
            and metadata$action='INSERT'
            and metadata$update='TRUE'
        then update
            set f.prd_code = s.prd_code
    13. delete use case: if it is deelte, metadata$_action column will show as delete ,metadata$update will show as false and the corresponding metadata$row_id
        merge into tgt_table f 
        using stream_object s
        on f.id = s.id
        when matched
            and metadata$action='DELETE'
            metadata$update='FALSE'
        then delete
    14. full process:
        create or replace task cus_insert1
        warehouse='name'
        schedule='1 MINUTE'
        when system$stream_has_data('stream name')
        as
        merge into tgt_table f 
        using stream_object s
        on f.id = s.id
        when matched # delete condition
            and metadata$action='DELETE'
            metadata$update='FALSE'
        then delete
        when matched #update condition
            and metadata$action='INSERT'
            and metadata$update='TRUE'
        then update
            set f.prd_code = s.prd_code
        when not matched #insert condition
            and and metadata$action='INSERT'
            then insert (id, prd_code)
            values (s.id, s.prd_code)

    15. types of streams. above one is standard / default : captures insert, update and    delete
        other ones is append only ; captures only inserts
        create stream stream_name on table src_tblname append_only = TRUE

    16. Change clause:
        create table;
        alter table tblname set change_tracking = true;

        select *from table
        changes(information => default)
        at (offset => 0.5*60) /see changes happend 30 secs ago

        select *from table
        changes(information => append_only)
        at (offset => 0.5*60) /see changes happend 30 secs ago


### M views ###

    1. materialized views
    2. freqently queries and long time to be processed
    3. create a MV
    4.  results will be stored in a sep table and this will be updated automatically based the base table.
    5. if data is chaning very freqently then do not consider MV but consider tasks & streams.
    6. joins(including self-joins) are not supported
    7. limited amount of agg functions
    8. udfs, having, orderBy and limit clause are not allowed.

### Data Masking ###

    1. create a role; 
    2. create or replace role analyst_masked; 
    3. create or replace role analyst_full;
    4. make sure role have access to warehouse, schema, db and table
    5. select grant on tables and usgae grants on schema and warehouse.
    6. create a policy
    7. create or replace masking policy phone
        as (val varchar) returns varchar ->
        case
        when current_role() in ('ANALYST_FULL', 'ACCOUNTADMIN') then val
        else '##-###-###'
        end;
    8. alter table if exists customers modify column phone set masking policy phone;
    9. use role analyst_full;
    10. select *from customers;
    11. use role analyst_masked;
    12. select *From customers;
    13. desc masking policy phone;
    14. show masking policies;
    15. drop masking policy phone;
    16. select *from table(information_Schema.policy_references(policy_name=>'phone'))
    17. alter masking policy phone set body ->
        case
        when current_role() in ('ANALYST_FULL', 'ACCOUNTADMIN') then val
        else '##-##-###'
        end;













