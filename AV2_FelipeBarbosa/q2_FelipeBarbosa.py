import threading

user = {
    "login": "felipe",
    "password": "1234",
    "cash": 27000
}

obj = lambda label, next : {"label": label, "next": next}

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
goToNode = lambda node, index : findByLabel(node['next'][index])
hasInput = lambda node : node['label'] in [receiveCash['label'], fundTransfer['label'], requestCreditAccountDetails['label']]
hasNextNode = lambda label : len(list(filter (lambda e : e['label'].lower() == label.lower(), nodes))) > 0
inputHandling = lambda node : print("R$" + str(1) + " serão utilizados para a transação.\n")
flowDecision = lambda decision : int(decision)-1
proceed = lambda fn, node : fn(node) if hasInput(node) == False else inputHandling(node)
checkEnd = lambda fn, node : fn(goToNode(node, flowDecision())) if node['next'] is not None else None
cannotProceed = lambda node : print("Não foi possível prosseguir para a atividade {}.".format(node['label']))
login = lambda username, password, beginFn : beginFn if username == user['login'] and password == user['password'] else cannotProceed

def system (node):
    print("--------------------------------")
    print(node['label'])
    proceed(lambda node : None, node)
    return system

#Três testes unitários de fluxos do diagrama
print("||||||||||||||||||||||||||||||||||\n|||||||||||||FLUXO 1||||||||||||||\n||||||||||||||||||||||||||||||||||")
system(createTransaction)(cash)(receiveCash)(printPaymentReceipt)(returnPaymentReceipt)(completeTransaction)(closeTransaction)
print("||||||||||||||||||||||||||||||||||\n|||||||||||||FLUXO 2||||||||||||||\n||||||||||||||||||||||||||||||||||")
system(createTransaction)(fundTransfer)(provideBankDepositDetails)(confirmPaymentApprovalFromBank)(closeTransaction)
print("||||||||||||||||||||||||||||||||||\n|||||||||||||FLUXO 3||||||||||||||\n||||||||||||||||||||||||||||||||||")
system(createTransaction)(credit)(requestCreditAccountDetails)(requestPaymentFromBank)(confirmPaymentApprovalFromBank)(closeTransaction)

execution = lambda fn, args: print(fn(args))
# Criando e iniciando as threads usando list comprehension. Utilizei o primeiro dos três fluxos acima. 
stress_level = lambda : 10000
threads = [threading.Thread(target=execution, args=(system(createTransaction)(cash)(receiveCash)(printPaymentReceipt)(returnPaymentReceipt)(completeTransaction), closeTransaction)) for _ in range(stress_level())]
starting_threads = lambda threads : [t.start() for t in threads]
joining_threads = lambda threads : [t.join() for t in threads]
starting_threads(threads)
joining_threads(threads)
print("Teste de stress concluído.")