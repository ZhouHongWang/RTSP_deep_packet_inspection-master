delimiter |

drop procedure if exists pro_select_tcpport;

create procedure pro_select_tcpport
(in s_ip varchar(15), in d_ip varchar(15), in s_port smallint unsigned, in d_port smallint unsigned, out result_count int)
begin
select count(*) 
into result_count
from rtsp_tcptb where sip=s_ip and dip=d_ip and sport=s_port and d_port;
end;
/*
drop procedure if exists pro_select_udpport;

create procedure pro_select_udpport
(in s_ip varchar(15), in d_ip varchar(15), out c_port json, out s_port json)
begin 
select client_port,server_port
into c_port,s_port
from rtsp_udptb where sip in (s_ip,d_ip) and dip in (s_ip,d_ip) and client_port is not null and server_port is not null;
end ;
*/
drop procedure if exists pro_select_udpport;

create procedure pro_select_udpport
(in s_ip varchar(15), in d_ip varchar(15))
begin 
select client_port,server_port from rtsp_udptb where sip in (s_ip,d_ip) and dip in (s_ip,d_ip);
end |

delimiter ;
