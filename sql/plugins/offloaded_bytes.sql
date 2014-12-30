CREATE TABLE `offloaded_bytes` (
	time	DATETIME NOT NULL,
	total_bytes	INT NOT NULL,
	offloaded	INT NOT NULL,
	percentage	INT NOT NULL,
	PRIMARY KEY(time)
);