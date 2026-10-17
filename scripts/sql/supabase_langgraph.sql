create schema if not exists langgraph;

create role langgraph_app login password 'YOUR_PASSWORD';

revoke all on schema public from langgraph_app;
grant usage, create on schema langgraph to langgraph_app;

alter default privileges in schema langgraph
  grant all on tables to langgraph_app;
alter default privileges in schema langgraph
  grant all on sequences to langgraph_app;

alter role langgraph_app set search_path = langgraph;