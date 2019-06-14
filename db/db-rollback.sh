#!/bin/bash
ROOT_PATH=$(cd $(dirname $0) && pwd);
cd $ROOT_PATH
liquibase --url='jdbc:postgresql://localhost:5432/beer?charSet=UTF8' --username=postgres --password=postgres --classpath=$POSTGRES_JDBC --logLevel=info --changeLogFile=src/changelog.xml rollback empty
