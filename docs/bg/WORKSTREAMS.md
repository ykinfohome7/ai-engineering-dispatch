# BGDB AI-EMDS — направления

> 🇧🇬 Седемте инженерни агента се използват във всички направления без дублиране.

## Области

> 🇧🇬 Към всеки проект има водещ агент, участници и независим проверяващ.

1. **Networking and Cybersecurity** — водещ architect; участници devops, developer-codex; проверяващ reviewer.
2. **Servers, DevOps and AI Infrastructure** — водещ devops; участници developer-claude-code, qa-tester; проверяващ reviewer.
3. **Telephony and Communications** — водещ architect; участници developer-codex, qa-tester; проверяващ reviewer.
4. **Business Software and ERP** — водещ developer-claude-code; участници developer-codex, qa-tester, docs; проверяващ reviewer.
5. **Transport and Logistics** — водещ architect; участници developer-claude-code, docs; проверяващ reviewer.
6. **Energy, AI and Data Centers** — водещ architect; участници developer-codex, docs; проверяващ reviewer.
7. **Research, Official Records and Documentation** — водещ docs; участници qa-tester, developer-codex; проверяващ reviewer.

## Ограничения

> 🇧🇬 Файловете са примерен план, а не активна защита или бюджет.

Не разрешавай автоматично внедряване, сливане към main, изтриване, работа по сървъри, публикуване на тайни, финансови операции или промяна на ключове. Реалните ограничения трябва да се включат и проверят в Paperclip, GitHub и KSSH.

## Създаване на проектите

> 🇧🇬 Без --apply няма заявки и не се създава нищо.

Изпълни python3 scripts/register-workstreams.py за dry-run. Когато постоянната Paperclip инстанция, организацията и разрешенията са готови, използвай python3 scripts/register-workstreams.py --apply. Създават се само липсващи проекти със статус planned. Агентите не се стартират.

## Преди Rebuild

> 🇧🇬 При пресъздаване на контейнера локалните данни могат да бъдат изгубени.

Прегледай docs/REBUILD-VERIFY.md и осигури проверено постоянно съхранение и възстановим архив на база, ключове и настройки, преди пълен Codespaces Rebuild.
