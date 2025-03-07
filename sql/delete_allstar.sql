delete from pr.CURRENT_GAME_LOGS
where GAME_DATE > '13-02-2025';
commit;
select distinct team from pr.CURRENT_GAME_LOGS;