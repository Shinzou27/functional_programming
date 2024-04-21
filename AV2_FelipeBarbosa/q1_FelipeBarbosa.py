# Desenvolva um programa em Python que implemente o diagrama de atividades acima.

user = {
    "login": "felipe",
    "password": "1234",
    "cash": 27000
}

obj = lambda label, next : {"label": label, "next": next}

#Criação dos nós do diagrama
createTransaction = obj("Create Transaction", ["Cash", "Credit", "Fund Transfer"])
cash = obj("Cash", ["Receive Cash"])
receiveCash = obj("Receive Cash", ["Print Payment Receipt"])
printPaymentReceipt = obj("Print Payment Receipt", ["Return Payment Receipt"])
returnPaymentReceipt = obj("Return Payment Receipt", ["Complete Transaction"])
completeTransaction = obj("Complete Transaction", None)

fundTransfer = obj("Fund Transfer", ["Provide Bank Deposit Details"])
provideBankDepositDetails = obj("Provide Bank Deposit Details", ["Confirm Payment Approval from Bank", "Cancel Transaction"])
confirmPaymentApprovalFromBank = obj("Confirm Payment Approval from Bank", ["Close Transaction"])
cancelTransaction = obj("Cancel Transaction", ["Close Transaction"])
closeTransaction = obj("Close Transaction", None)

credit = obj("Credit", ["Request Credit Account Details"])
requestCreditAccountDetails = obj("Request Credit Account Details", ["Request Payment from Bank"])
requestPaymentFromBank = obj("Request Payment From Bank", ["Confirm Payment Approval from Bank", "Cancel Transaction"])

nodes = [createTransaction, cash, receiveCash, printPaymentReceipt,
         returnPaymentReceipt, completeTransaction, fundTransfer,
         provideBankDepositDetails, confirmPaymentApprovalFromBank,
         cancelTransaction, closeTransaction, credit, requestCreditAccountDetails,
         requestPaymentFromBank]

findByLabel = lambda label : list(filter (lambda e : e['label'].lower() == label.lower(), nodes))[0]
getNextNode = lambda node, label : findByLabel(label) if label in node['next'] else "O nó não possui conexão com a opção escolhida."
showOptions = lambda node : print("\n".join("{} ({})".format(node['next'][i], i+1) for i in range(len(node['next'])))) if node['next'] is not None else print("Fim do fluxo.")
# Caso não receba um índice válido, escolherá a primeira opção.
goToNode = lambda node, index : findByLabel(node['next'][0]) if str(index).isnumeric() == False or len(node['next']) < int(index)-1 else findByLabel(node['next'][int(index)-1])
hasInput = lambda node : node['label'] in [receiveCash['label'], fundTransfer['label'], requestCreditAccountDetails['label']]
hasNextNode = lambda label : len(list(filter (lambda e : e['label'].lower() == label.lower(), nodes))) > 0
def inputHandling(node):
    print("R$" + input("Insira a quantidade a ser retirada:\n") + " serão utilizados para a transação.\n")
    showOptions(node)
flowDecision = lambda : input("Digite a operação a seguir.\n")
proceed = lambda fn, node : fn(node) if hasInput(node) == False else inputHandling(node)
checkEnd = lambda fn, node : fn(goToNode(node, flowDecision())) if node['next'] is not None else None
cannotProceed = lambda node : print("Não foi possível prosseguir para a atividade {}.".format(node['label']))
login = lambda username, password, beginFn : beginFn if username == user['login'] and password == user['password'] else cannotProceed

def system (node):
    print("--------------------------------")
    print(node['label'])
    proceed(showOptions, node)
    checkEnd(system, node)
    
login(input("Digite seu username.\n"), input("Digite sua senha.\n"), system)(createTransaction)
