      SUBROUTINE TRANS
      IMPLICIT REAL*8(A-H,O-Z)
      DIMENSION AM(8),CA15(8),CA2(8),CA25(8),CA3(8),CA4(8)
      COMMON/ICOU/VOLN,SOBS,RJA1,RJA2,ICOUNT,NGOL,NHBS
      COMMON/GEOM1/XB(240),RB(240),RBP(240),C2,BETA
      COMMON/GEO3/VOVS,AL,YINT,F,RR,RREF,AREF,DLN
      COMMON/NNI/NTT(11),NP5,JZT
      COMMON/GEO2/NFL,NN,IPRINT,MAL,MAX,IPR
      COMMON/CVP/CXT(240),CNT(240),CMT(240),CPV(21),JA,JB,KF
      COMMON/DISC/R1,PI,I,JH,J,KL
      COMMON/RX/XR(20,6),G(20),GCH,DM,N,N1(20),IX,I1
      COMMON/DIS2/SUM1,SUM2,SUM3,SUM4,SUM5,SUM6
      COMMON/LENG/BL,ANL,ALA
      COMMON/WAVE/CABL,CNBL,CMBL,CAW,CNW,CMW
      DATA AM/.85,.9,.95,1.,1.05,1.1,1.15,1.2/
      DATA CA15/.01,.072,.13,.177,.215,.247,.277,.3/
      DATA CA2/0.,.036,.073,.107,.14,.169,.191,.205/
      DATA CA25/0.,.01,.04,.07,.098,.122,.138,.143/
      DATA CA3/0.,0.,.024,.048,.073,.092,.102,.097/
      DATA CA4/0.,0.,.01,.032,.047,.055,.055,.04/
      IF(NHBS.NE.N) GO TO 87
      CBO=0.D0
      GO TO 88
  87  VOV=VOVS
      IF(VOV.LT.1) VOV=1.D0
      AREF=PI*RREF**2
      GAMA=1.4D0
      C1=1.D0+GAMA
      C0=DSQRT(C1)
      C3=VOV**2
      C4=1.D0-C3
      C5=C4/(C1*C3)
      C7=25.D0*C1*VOV**(2.D0/3.D0)
      C8=.5D0*C4/(C1*C3)
      C9=1.25D0*C5**2
      J=NTT(NHBS)+1
      DO 10 I=J,NN
      XX=XB(I)-XB(J)
      DELTA=DATAN(1.D0/(2.D0*ANL))
      IF(RBP(J-3).LT.RBP(1))DELTA=DATAN(.2D0/ANL)
      C6=3.D0*DELTA/(2.D0*C0)
      C10=2.D0*C5*(C6**2)**(1.D0/3.D0)/VOV**(2.D0/3.D0)
      C11=((C6/VOV)**4)**(1.D0/3.D0)
      CSQ=C7*(C8+(C9+C10+C11)**(0.5))
      C=DSQRT(CSQ)
      Y=2.D0*ALA+2.D0*XX
      CP1=.4D0*(Y-C)/DSQRT(C1*VOV**(2.D0/3.D0))*(.04D0*
     *(Y-C)**2/(C1*VOV**(2.D0/3.D0
     *))-C4/(C1*C3))**(.5D0)
      IF(Y.GT.C) CP1=0.D0
      DELTA=RBP(I)
      C6=3.D0*DELTA/(2.D0*C0)
      C10=2.D0*C5*(C6**2)**(1.D0/3.D0)/VOV**(2.D0/3.D0)
      C11=((C6/VOV)**4)**(1.D0/3.D0)
      CSQ=C7*(C8+(C9+C10+C11)**(0.5D0))
      C=DSQRT(CSQ)
      Y=XX*2.D0
      CPV(1)=0.4D0*(Y-C)/DSQRT(C1*VOV**(2.D0/3.D0))*
     *(.04D0*(Y-C)**2/(C1*VOV**(2
     *.D0/3.D0))-C4/(C1*C3))**(.5D0)-DELTA**2+CP1
      IF(Y.GT.C)CPV(1)=CP1
      IF(IPRINT.NE.1)GO TO 15
   15 DO 11 K1=1,KF
      CPV(K1)=CPV(1)
 11   END DO
      CALL POPIN
 10   END DO
      JA=J
      JB=NN
      CALL SIMP
      IF(VOVS.GE.0.95D0) GO TO 90
      CBO=0.D0
      GO TO 88
  90  CBO=2.D0*SUM1/AREF
      CBO=CBO*(VOVS-0.95D0)/(VOV-0.95D0)
 88   CONTINUE
      CALL INTERP(AM,CA15,VOVS,A0,8,3)
      CALL INTERP(AM,CA2,VOVS,A1,8,3)
      CALL INTERP(AM,CA25,VOVS,A2,8,3)
      CALL INTERP(AM,CA3,VOVS,A3,8,3)
      CALL INTERP(AM,CA4,VOVS,A4,8,3)
      AN1=ANL*DEXP(-0.004D0*ANL**1.75D0)
      IF(AN1.LE.4.D0)GO TO 16
      CAN=A4*(1.D0-.2D0*(AN1-4.D0))
      GO TO 17
 16   CALL INTER5(AN1,1.5D0,2.D0,2.5D0,3.D0,4.D0,
     *A0,A1,A2,A3,A4,CAN)
 17   CAW=CAN+CBO
      RETURN
      END
