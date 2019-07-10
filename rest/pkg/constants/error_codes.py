ERROR_INTERNAL_EXCEPTION = -32001
ERROR_DATABASE_EXCEPTION = -32002
ERROR_JSON_PARSING_EXCEPTION = -32003
ERROR_INCORRECT_PASSWORD = -32004
ERROR_INVALID_USER_OR_PASSWORD = -32005
ERROR_JWT_EXCEPTION = -32006

ERROR_UNALLOWED_CARD_TYPE = -33001

ERROR_TEXT_MAP = {
    ERROR_INTERNAL_EXCEPTION: 'Internal exception',
    ERROR_DATABASE_EXCEPTION: 'Database exception',
    ERROR_JSON_PARSING_EXCEPTION: 'Failed when parsing body as json',
    ERROR_INCORRECT_PASSWORD: 'Incorrect password',
    ERROR_INVALID_USER_OR_PASSWORD: 'Invalid user ID or password',

    ERROR_UNALLOWED_CARD_TYPE: 'Unallowed card type for this operation',
}
