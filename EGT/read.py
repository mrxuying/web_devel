#
def read_urls():
      f = open('D:\\github\\EGT\\conf\\config.txt','rb')
      fp = f.readlines()
      #print(type(fp))
      #print(fp)
      f.close()
      urls = []
      ports = []
      for date in fp:
            m,n = date.split(','.encode(encoding='utf-8'))
            k = m.strip('\t\r\n'.encode(encoding='utf-8'))
            h = n.strip('\t\r\n'.encode(encoding='utf-8'))
            urls.append(k)
            ports.append(h)
            #print(urls)

      return urls,ports

def read_users():
    f = open('D:\\github\\EGT\\conf\\users.txt','rb')
    fp = f.readlines()
    #print(fp)
    f.close()
    users = []
    pwds = []
    for date in fp:
          m,n = date.split(','.encode(encoding='utf-8'))
          k = m.strip('\t\r\n'.encode(encoding='utf-8'))
          h = n.strip('\t\r\n'.encode(encoding='utf-8'))
          users.append(k)
          pwds.append(h)

    return users,pwds

# if __name__ == '__main__':
#     read_urls()
