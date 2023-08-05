class Response_json:
    def __init__(self):
        self.f_v = 0
        self.f_m = 0
        self.h_v = 0
        self.h_m = 0
    
    # features[1] = 1 (femme) / = 0 (homme) 
    # target[0] = 1 (survived) / = 0 (dead)
    def sex_survived(self, X, y):
        for features, target in zip(X.values, y.values):
            if int(features[1]) == 1 and target[0] == 1:
                self.f_v += 1
            elif int(features[1]) == 1 and target[0] == 0:
                self.f_m += 1
            elif int(features[1]) == 0 and target[0] == 1:
                self.h_v += 1
            elif int(features[1]) == 0 and target[0] == 0:
                self.h_m += 1
        return [{"name":"Nombre de femmes ayant survécu","pourcent":self.f_v},{"name":"Nombre de femmes n'ayant pas survécu", "pourcent":self.f_m},{"name":"Nombre d'hommes ayant survécu", "pourcent":self.h_v},{"name":"Nombre d'hommes n'ayant pas survécu", "pourcent":self.h_m}]       
        


