--
-- ATLAS Exposure Statistics
-- Created as a cache of the number of detections in each exposure and subcell.
-- Can be recreated if necessary - so no need to backup this table.
--
drop table if exists `atlas_diff_subcells`;

create table `atlas_diff_subcells` (
`id` bigint unsigned not null auto_increment,
`obs` varchar(60),
`region` smallint unsigned not null,
`ndet` int unsigned not null,
PRIMARY KEY `pk_id` (`id`),
UNIQUE KEY `idx_obs_region` (`obs`, `region`),
KEY `idx_obs` (`obs`),
KEY `idx_region` (`region`)
) ENGINE=MyISAM;
