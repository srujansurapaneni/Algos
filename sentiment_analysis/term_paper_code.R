# data ingestion and clean_up

myvars <- c("CASEID","YEAR","AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB1","FREQ1","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_2014 <- teds_a_2014[myvars]
mydata_2014$uid <- rep(paste(mydata_2014$CASEID,mydata_2014$YEAR),nrow(mydata_2014))

myvars <- c("CASEID","YEAR","AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB1","FREQ1","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_2012 <- da35037.0001[myvars]

myvars <- c("CASEID","YEAR","AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB1","FREQ1","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_2011 <- da34876.0001[myvars]

myvars <- c("CASEID","YEAR","AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB1","FREQ1","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_2010 <- da33261.0001[myvars]

mydata_full <- rbind(mydata_2010,mydata_2011,mydata_2012,mydata_2014)

mydata_sub2010 <- mydata_2010[mydata_2010$SUB1=="(7) OTHER OPIATES AND SYNTHETICS",]
mydata_sub2011 <- mydata_2011[mydata_2011$SUB1=="(7) OTHER OPIATES AND SYNTHETICS",]
mydata_sub2012 <- mydata_2012[mydata_2012$SUB1=="(7) OTHER OPIATES AND SYNTHETICS",]
mydata_sub2014 <- mydata_2014[mydata_2014$SUB1=="OTHER OPIATES AND SYNTHETICS",]

mydata_sub <- na.omit(rbind(mydata_sub2010,mydata_sub2011,mydata_sub2012,mydata_sub2014))
mydata_sub$uid <- rep(paste(mydata_sub$CASEID,mydata_sub$YEAR))

myvars2 <- c("AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","uid")
mydata_sub_uid <- mydata_sub[myvars2]

x <- count(mydata_sub_uid,c("AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS"))

myvarspre <- c("AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB1","FREQ1","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_pre <- mydata_sub[myvarspre]

mydata_train <- merge(mydata_pre,x,by=c("AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS"))

myvarspost <- c("CASEID","AGE","GENDER","MARSTAT","EMPLOY","LIVARAG","STFIPS","SUB2","FREQ2","SUB3","FREQ3","OPSYNFLG","ALCDRUG","DSMCRIT","PSYPROB")
mydata_test <- da30462.0001[myvarspost]
mydata_test1<- mydata_test
mydata_test <- x

# Analysis and predictions
model <- glm(SUB1~AGE+GENDER+MARSTAT+EMPLOY+LIVARAG+OPSYNFLG+ALCDRUG+DSMCRIT+PSYPROB,
                                         data=mydata_train,
                                         family=binomial(link="logit")
                                         )
summary(model)
result <- predict(model,data=mydata_test,type='response')

