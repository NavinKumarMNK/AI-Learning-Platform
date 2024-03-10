FROM cassandra

COPY init-cassandra.sh /init-cassandra.sh
RUN chmod +x /init-cassandra.sh
EXPOSE 9042

ENTRYPOINT [ "/init-cassandra.sh" ]

CMD ["cassandra", "-f"]