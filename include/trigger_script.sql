DELIMITER $$
USE `flow_db`$$

drop trigger if exists rtsp_tcptb_BEFORE_DELETE;
CREATE DEFINER=`root`@`localhost` TRIGGER `rtsp_tcptb_BEFORE_DELETE` BEFORE DELETE ON `rtsp_tcptb` FOR EACH ROW BEGIN
insert ignore into rtsp_tcptb_backup
values(old.sip,old.dip,old.sport,old.dport,old.session,old.starttime,current_timestamp);
END$$

drop trigger if exists rtsp_udptb_BEFORE_DELETE;

CREATE DEFINER=`root`@`localhost` TRIGGER `rtsp_udptb_BEFORE_DELETE` BEFORE DELETE ON `rtsp_udptb` FOR EACH ROW BEGIN
insert ignore into rtsp_udptb_backup 
values (old.sip,old.dip,old.sport,old.dport,old.session,old.starttime,current_timestamp,old.client_port,old.server_port);
END$$

DELIMITER ;