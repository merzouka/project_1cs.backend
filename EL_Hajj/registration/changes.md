# Payment/Appointment
- status should have 3 states, the default is null, accepted = true, denied = false
- should return winner status with response to winners fetch in case of changes on multiple sessions by user
- use `@renderer_classes([JSONRenderer]) + Response` combination to return value rather than `JsonResponse`
- use `PATCH` method for status update as it is more appropriate (the manager is _updating_ the status of the winner)
- don't send redundant user id info
- [not changed in code] return just id the consumer of the api doesn't need to know what the id is used for

