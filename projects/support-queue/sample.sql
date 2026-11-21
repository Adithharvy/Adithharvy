CREATE TABLE tickets (
    ticket_id INTEGER PRIMARY KEY,
    queue TEXT NOT NULL,
    opened TEXT NOT NULL,
    resolved TEXT,
    CHECK (resolved IS NULL OR resolved >= opened)
);

-- Fictional UTC timestamps. Ticket 8 closes after the reporting cutoff.
INSERT INTO tickets VALUES
(1,'Accounts','2026-10-01 08:00','2026-10-01 10:00'),
(2,'Accounts','2026-10-01 09:00','2026-10-02 09:00'),
(3,'Accounts','2026-10-02 06:00',NULL),
(4,'Payments','2026-10-01 12:00',NULL),
(5,'Payments','2026-10-02 08:00','2026-10-02 14:00'),
(6,'Mobile','2026-10-02 12:00','2026-10-02 13:00'),
(7,'Mobile','2026-10-04 09:00',NULL),
(8,'Payments','2026-10-02 18:00','2026-10-03 12:00');
