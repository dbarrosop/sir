CREATE TABLE best_prefixes
(
    ip_dst TEXT NOT NULL,
    mask_dst INTEGER NOT NULL,
    packets INTEGER NOT NULL,
    bytes INTEGER NOT NULL,
    stamp_updated TEXT NOT NULL,
    PRIMARY KEY (ip_dst, mask_dst, stamp_updated)
);
