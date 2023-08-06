salario = float(input()) 



if (salario >= 0 and salario <= 600.00):
  aumento = salario * 17 / 100
  aumento_salarial = salario + aumento

  aumento = str(aumento)
  virgula_aumento = aumento.replace(".",",")
  aumento_salarial = str(aumento_salarial)
  virgula_aumento_salarial = aumento_salarial.replace(".",",")

  print(f"Novo salario: {virgula_aumento_salarial} Reajuste ganho: {virgula_aumento} Em percentual: 17 %")


elif (salario >= 600.01 and salario <= 900.00):
  aumento = salario * 13 / 100
  aumento_salarial = salario + aumento 
  
  aumento = str(aumento)
  virgula_aumento = aumento.replace(".",",")
  aumento_salarial = str(aumento_salarial)
  virgula_aumento_salarial = aumento_salarial.replace(".",",")

  print(f"Novo salario: {virgula_aumento_salarial} Reajuste ganho: {virgula_aumento} Em percentual: 13 %")



elif (salario >= 900.01 and salario <= 1500.00):
  aumento = salario * 12 / 100
  aumento_salarial = salario + aumento 

  aumento = str(aumento)
  virgula_aumento = aumento.replace(".",",")
  aumento_salarial = str(aumento_salarial)
  virgula_aumento_salarial = aumento_salarial.replace(".",",")

  print(f"Novo salario: {virgula_aumento_salarial} Reajuste ganho: {virgula_aumento} Em percentual: 12 %")

  
elif (salario >= 1500.01 and salario <= 2000.00):
  aumento = salario * 10 / 100
  aumento_salarial = salario + aumento 
  aumento = str(aumento)

  virgula_aumento = aumento.replace(".",",")
  aumento_salarial = str(aumento_salarial)
  virgula_aumento_salarial = aumento_salarial.replace(".",",")

  print(f"Novo salario: {virgula_aumento_salarial} Reajuste ganho: {virgula_aumento} Em percentual: 10 %")

  
else: 
  aumento = salario * 5 / 100
  aumento_salarial = salario + aumento 

  aumento = str(aumento)
  virgula_aumento = aumento.replace(".",",")
  aumento_salarial = str(aumento_salarial)
  virgula_aumento_salarial = aumento_salarial.replace(".",",")

  print(f"Novo salario: {virgula_aumento_salarial} Reajuste ganho: {virgula_aumento} Em percentual: 5 %")