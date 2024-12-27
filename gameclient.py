import socket
import random

decknomes=["As","2","3","4","5","6","7","8","9","10","Valete","Rainha","Rei"]
condicao=["maior impar","maior par","menor impar","menor par"]
dados= socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def pescar(vezes=1):
	mao=[]
	for x in range(vezes):
		carta=dados.recv(1)
		carta=int.from_bytes(bytes=carta, byteorder='big', signed=False)
		mao.append(carta)
	return mao

def printmao(mao):
	maon=""
	for x in range(len(mao)):
		maon+=decknomes[mao[x]]
		maon+=' '
	print(maon)

def main():
	
	porta=42069
	ip="127.0.0.1"
	dados.connect((ip,porta))
	
	pontos=[0,0]
	mao=pescar(3)
	while pontos[0]<2 and pontos[1]<2:
		cond=dados.recv(1)
		cond=int.from_bytes(bytes=cond, byteorder='big', signed=False)
		print("condicao de vitoria:")
		print(condicao[cond])
		print("sua mao:")
		printmao(mao)
		cardesc=int(input("escolha um card:(1-3)\n"))
		cardesc=mao[cardesc-1]
		mao.remove(cardesc)
		pacote=cardesc.to_bytes(length=1,byteorder='big',signed=False)
		dados.send(pacote)
		r=dados.recv(1)
		r=int.from_bytes(bytes=r, byteorder='big', signed=False)
		if r==0:
			print("empate!")
		else:
			print("o jogador "+str(r)+" ganhou")
			pontos[r-1]+=1;
		mao.extend(pescar(1))
		print("pontuacao: "+str(pontos))
	if pontos[1]==2:
		print("Voce ganhou a partida")
	else:
		print("Voce perdeu a partida")

if __name__ == '__main__':
    main()