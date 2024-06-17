import random

def generate_cpf(has_punctuation: bool = False):                                                        
    cpf = [random.randint(0, 9) for x in range(9)]                              
                                                                                
    for _ in range(2):                                                          
        val = sum([(len(cpf) + 1 - i) * v for i, v in enumerate(cpf)]) % 11      
                                                                                
        cpf.append(11 - val if val > 1 else 0)
        
    if has_punctuation:
        return '%s%s%s.%s%s%s.%s%s%s-%s%s' % tuple(cpf)                   
                                                                                
    return '%s%s%s%s%s%s%s%s%s%s%s' % tuple(cpf)

def generate_cnpj(has_punctuation: bool = False):                                                       
    def calculate_special_digit(l):                                             
        digit = 0                                                               
                                                                                
        for i, v in enumerate(l):                                               
            digit += v * (i % 8 + 2)                                            
                                                                                
        digit = 11 - digit % 11                                                 
                                                                                
        return digit if digit < 10 else 0                                       
                                                                                
    cnpj =  [1, 0, 0, 0] + [random.randint(0, 9) for x in range(8)]             
                                                                                
    for _ in range(2):                                                          
        cnpj = [calculate_special_digit(cnpj)] + cnpj
        
    if has_punctuation:
        return '%s%s.%s%s%s.%s%s%s/%s%s%s%s-%s%s' % tuple(cnpj[::-1])         
                                                                                
    return '%s%s%s%s%s%s%s%s%s%s%s%s%s%s' % tuple(cnpj[::-1])

test = generate_cnpj()
print(test)